import {env} from "cloudflare:workers";

type YouTubeEnv={YOUTUBE_API_KEY?:string};
type ApiItem={id:string;snippet?:Record<string,any>;statistics?:Record<string,string>;contentDetails?:Record<string,any>};

const number=(value?:string)=>Number(value)||0;
const average=(values:number[])=>values.length?values.reduce((sum,value)=>sum+value,0)/values.length:0;

async function youtube(path:string,params:Record<string,string>,key:string){
  const url=new URL(`https://www.googleapis.com/youtube/v3/${path}`);
  Object.entries({...params,key}).forEach(([name,value])=>url.searchParams.set(name,value));
  const response=await fetch(url,{headers:{accept:"application/json"}});
  const body=await response.json() as {items?:ApiItem[];error?:{message?:string}};
  if(!response.ok)throw new Error(body.error?.message||`YouTube returned ${response.status}`);
  return body.items||[];
}

export async function GET(request:Request){
  const key=(env as unknown as YouTubeEnv).YOUTUBE_API_KEY;
  if(!key)return Response.json({error:"YouTube connector is not configured",code:"connector_not_configured"},{status:503});
  const channelId=new URL(request.url).searchParams.get("channelId")?.trim()||"";
  if(!/^UC[\w-]{22}$/.test(channelId))return Response.json({error:"Enter a valid 24-character YouTube channel ID"},{status:400});
  try{
    const channels=await youtube("channels",{part:"snippet,statistics,contentDetails",id:channelId},key);
    const channel=channels[0];if(!channel)return Response.json({error:"YouTube channel was not found"},{status:404});
    const uploads=channel.contentDetails?.relatedPlaylists?.uploads as string|undefined;
    const playlist=uploads?await youtube("playlistItems",{part:"contentDetails",playlistId:uploads,maxResults:"10"},key):[];
    const ids=playlist.map(item=>item.contentDetails?.videoId as string).filter(Boolean);
    const videos=ids.length?await youtube("videos",{part:"snippet,statistics",id:ids.join(",")},key):[];
    const views=videos.map(video=>number(video.statistics?.viewCount)),likes=videos.map(video=>number(video.statistics?.likeCount)),comments=videos.map(video=>number(video.statistics?.commentCount));
    const avgViews=average(views),avgLikes=average(likes),avgComments=average(comments),engagementRate=avgViews?((avgLikes+avgComments)/avgViews)*100:0;
    const statistics=channel.statistics||{},snippet=channel.snippet||{},fetchedAt=new Date().toISOString();
    return Response.json({source:"youtube_data_api_v3",fetchedAt,channel:{id:channel.id,title:snippet.title,description:snippet.description,customUrl:snippet.customUrl,subscribers:number(statistics.subscriberCount),videoCount:number(statistics.videoCount),totalViews:number(statistics.viewCount),thumbnail:snippet.thumbnails?.default?.url},metrics:{sampleSize:videos.length,avgViews,avgLikes,avgComments,engagementRatePct:engagementRate},recentVideos:videos.map(video=>({id:video.id,title:video.snippet?.title,publishedAt:video.snippet?.publishedAt,views:number(video.statistics?.viewCount),likes:number(video.statistics?.likeCount),comments:number(video.statistics?.commentCount)}))});
  }catch(error){return Response.json({error:error instanceof Error?error.message:"YouTube data could not be loaded"},{status:502});}
}
