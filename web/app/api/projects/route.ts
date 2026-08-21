import { and, desc, eq } from "drizzle-orm";
import { getChatGPTUser } from "../../chatgpt-auth";
import { getDb } from "../../../db";
import { savedProjects } from "../../../db/schema";

export async function GET() {
  const user=await getChatGPTUser();if(!user)return Response.json({error:"Sign in required"},{status:401});
  const rows=await getDb().select().from(savedProjects).where(eq(savedProjects.userId,user.userId)).orderBy(desc(savedProjects.updatedAt)).limit(20);
  return Response.json({projects:rows.map(row=>({...row,payload:JSON.parse(row.payload)})),user:{displayName:user.displayName}});
}

export async function POST(request:Request){
  const user=await getChatGPTUser();if(!user)return Response.json({error:"Sign in required"},{status:401});
  const body=await request.json() as {name?:string;payload?:unknown};const name=body.name?.trim();if(!name||!body.payload||typeof body.payload!=="object")return Response.json({error:"Project name and payload are required"},{status:400});
  const payload=JSON.stringify(body.payload);if(payload.length>500000)return Response.json({error:"Project is too large to save"},{status:413});
  const project={id:crypto.randomUUID(),userId:user.userId,name:name.slice(0,80),payload};await getDb().insert(savedProjects).values(project);return Response.json({project:{...project,payload:body.payload}},{status:201});
}

export async function DELETE(request:Request){
  const user=await getChatGPTUser();if(!user)return Response.json({error:"Sign in required"},{status:401});const id=new URL(request.url).searchParams.get("id");if(!id)return Response.json({error:"Project id is required"},{status:400});await getDb().delete(savedProjects).where(and(eq(savedProjects.id,id),eq(savedProjects.userId,user.userId)));return Response.json({ok:true});
}
