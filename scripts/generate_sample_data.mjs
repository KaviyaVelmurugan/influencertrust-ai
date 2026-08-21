import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDirectory, "..");
const outputDir = path.join(projectRoot, "data", "sample");

let state = 20260821;
function random() {
  state = (state * 1664525 + 1013904223) >>> 0;
  return state / 4294967296;
}

function pick(values) {
  return values[Math.floor(random() * values.length)];
}

function integer(min, max) {
  return Math.floor(random() * (max - min + 1)) + min;
}

function decimal(value, places = 2) {
  return Number(value.toFixed(places));
}

function csvEscape(value) {
  const text = value === null || value === undefined ? "" : String(value);
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function toCsv(headers, rows) {
  return [headers, ...rows]
    .map((row) => row.map(csvEscape).join(","))
    .join("\n") + "\n";
}

const campaigns = [
  ["CAM-001", "EcoGlow Summer Launch", "awareness", "Plant-based SPF skincare", "India", "en", "skincare|sustainability|summer", "skin whitening|competitor-x", "#EcoGlow|#SummerSkin", "@ecoglow", "https://example.com/ecoglow", "#ad", 500000, 1800, "2026-09-01", "2026-09-30", "INR"],
  ["CAM-002", "PulseFit Challenge", "conversions", "At-home fitness membership", "India", "en", "fitness|wellness|home workout", "unsafe weight loss|steroids", "#PulseFit30", "@pulsefit", "https://example.com/pulsefit", "#sponsored", 750000, 2999, "2026-10-01", "2026-10-31", "INR"],
  ["CAM-003", "WanderLite Weekends", "traffic", "Affordable weekend travel packages", "India", "en", "travel|budget trips|local experiences", "dangerous travel|trespassing", "#WanderLite", "@wanderlite", "https://example.com/wanderlite", "Paid partnership", 600000, 12500, "2026-11-01", "2026-11-30", "INR"],
];

const categories = ["beauty", "fitness", "travel", "food", "technology", "fashion"];
const platforms = ["instagram", "youtube", "tiktok"];
const locations = ["Bengaluru", "Chennai", "Delhi", "Hyderabad", "Kochi", "Mumbai", "Pune"];
const topicMap = {
  beauty: "skincare|beauty routines|sustainable products",
  fitness: "fitness|wellness|home workout",
  travel: "travel|budget trips|local experiences",
  food: "recipes|restaurants|healthy food",
  technology: "consumer tech|apps|productivity",
  fashion: "style|ethical fashion|streetwear",
};

const influencers = [];
for (let index = 1; index <= 30; index += 1) {
  const category = categories[(index - 1) % categories.length];
  const platform = platforms[(index - 1) % platforms.length];
  const followers = integer(12000, 850000);
  const baseEngagement = 0.006 + random() * 0.075;
  const suspicious = index % 10 === 0;
  const averageLikes = Math.max(20, Math.round(followers * (suspicious ? 0.0015 : baseEngagement * 0.82)));
  const averageComments = Math.max(2, Math.round(followers * (suspicious ? 0.00008 : baseEngagement * 0.08)));
  const averageViews = Math.round(followers * (0.12 + random() * 1.25));
  const averageShares = Math.max(1, Math.round(averageViews * (0.001 + random() * 0.012)));
  const engagementRate = ((averageLikes + averageComments) / followers) * 100;
  const followerGrowth = suspicious ? 45 + random() * 70 : -1 + random() * 12;
  const fee = Math.round((followers * (0.25 + random() * 0.55)) / 1000) * 1000;
  const handle = `creator_${String(index).padStart(2, "0")}`;
  influencers.push([
    `INF-${String(index).padStart(3, "0")}`,
    handle,
    platform,
    category,
    `${category} creator sharing practical ${topicMap[category].replaceAll("|", ", ")}`,
    locations[(index - 1) % locations.length],
    index % 9 === 0 ? "hi" : "en",
    followers,
    integer(180, 4200),
    averageLikes,
    averageComments,
    averageViews,
    averageShares,
    decimal(followerGrowth),
    decimal(engagementRate),
    fee,
    "INR",
    topicMap[category],
  ]);
}

const captions = {
  beauty: ["My simple summer skincare routine with mindful product choices", "Three habits that helped me protect and hydrate my skin"],
  fitness: ["A realistic home workout you can complete in twenty minutes", "Consistency matters more than perfection in your wellness routine"],
  travel: ["A practical weekend itinerary with local experiences and a small budget", "Save this guide for your next short trip"],
  food: ["A quick balanced recipe for busy weekdays", "Trying a local restaurant and sharing my honest review"],
  technology: ["Testing a productivity app for one full week", "What I liked and disliked about this everyday gadget"],
  fashion: ["Styling one ethical fashion piece in three different ways", "A comfortable streetwear look for a long day"],
};

const posts = [];
let postNumber = 1;
for (const influencer of influencers) {
  const [influencerId, handle, , category, , , , , , avgLikes, avgComments, avgViews, avgShares] = influencer;
  for (let postIndex = 0; postIndex < 3; postIndex += 1) {
    const sponsored = postIndex === 2;
    const baseCaption = captions[category][postIndex % 2];
    const caption = sponsored
      ? `${baseCaption}. #ad #${category} @samplebrand`
      : `${baseCaption}. #${category}`;
    posts.push([
      `POST-${String(postNumber).padStart(4, "0")}`,
      influencerId,
      `2026-${String(5 + postIndex).padStart(2, "0")}-${String((postNumber % 25) + 1).padStart(2, "0")}`,
      caption,
      Math.max(0, Math.round(avgLikes * (0.72 + random() * 0.62))),
      Math.max(0, Math.round(avgComments * (0.65 + random() * 0.75))),
      Math.max(0, Math.round(avgViews * (0.70 + random() * 0.65))),
      Math.max(0, Math.round(avgShares * (0.60 + random() * 0.90))),
      sponsored,
    ]);
    postNumber += 1;
  }
}

const outcomes = [];
for (let index = 0; index < 12; index += 1) {
  const campaign = campaigns[index % campaigns.length];
  const influencer = influencers[(index * 2) % influencers.length];
  const impressions = integer(18000, 480000);
  const clicks = Math.round(impressions * (0.008 + random() * 0.035));
  const conversions = Math.round(clicks * (0.012 + random() * 0.065));
  const averageOrderValue = campaign[13];
  outcomes.push([
    `OUT-${String(index + 1).padStart(3, "0")}`,
    campaign[0],
    influencer[0],
    impressions,
    clicks,
    conversions,
    conversions * averageOrderValue,
    influencer[15],
    integer(5000, 25000),
    "INR",
  ]);
}

const submissionTopics = {
  "CAM-001": "A summer skincare routine featuring sustainable product choices",
  "CAM-002": "A fitness and wellness home workout challenge",
  "CAM-003": "A budget travel guide focused on local experiences",
};
const submissions = outcomes.map((outcome, index) => {
  const campaign = campaigns.find((item) => item[0] === outcome[1]);
  const variant = index % 4;
  const required = `${campaign[8].replaceAll("|", " ")} ${campaign[9].replaceAll("|", " ")} ${campaign[10]}`;
  let caption;
  if (variant === 0) {
    caption = `${submissionTopics[campaign[0]]}. ${required} ${campaign[11]}`;
  } else if (variant === 1) {
    caption = `${submissionTopics[campaign[0]]}. ${required}`;
  } else if (variant === 2) {
    caption = `${submissionTopics[campaign[0]]}. ${required} ${campaign[11]} ${campaign[7].split("|")[0]}`;
  } else {
    caption = `Sharing a quick update with my audience. ${campaign[8].split("|")[0]}`;
  }
  return [
    `SUB-${String(index + 1).padStart(3, "0")}`,
    outcome[1],
    outcome[2],
    caption,
  ];
});

const datasets = [
  {
    filename: "campaigns.csv",
    headers: ["campaign_id", "campaign_name", "objective", "product_description", "target_location", "target_language", "target_topics", "prohibited_terms", "required_hashtags", "required_mentions", "required_links", "required_disclosure", "budget", "average_order_value", "start_date", "end_date", "currency"],
    rows: campaigns,
  },
  {
    filename: "influencers.csv",
    headers: ["influencer_id", "handle", "platform", "category", "profile_text", "location", "primary_language", "followers", "following", "average_likes", "average_comments", "average_views", "average_shares", "follower_growth_30d_pct", "engagement_rate_pct", "estimated_fee", "currency", "content_topics"],
    rows: influencers,
  },
  {
    filename: "posts.csv",
    headers: ["post_id", "influencer_id", "published_at", "caption", "likes", "comments", "views", "shares", "is_sponsored"],
    rows: posts,
  },
  {
    filename: "outcomes.csv",
    headers: ["outcome_id", "campaign_id", "influencer_id", "impressions", "clicks", "conversions", "attributed_revenue", "influencer_fee", "production_cost", "currency"],
    rows: outcomes,
  },
  {
    filename: "campaign_submissions.csv",
    headers: ["submission_id", "campaign_id", "influencer_id", "caption"],
    rows: submissions,
  },
];

await fs.mkdir(outputDir, { recursive: true });

for (const dataset of datasets) {
  const csv = toCsv(dataset.headers, dataset.rows);
  const outputPath = path.join(outputDir, dataset.filename);
  await fs.writeFile(outputPath, csv, "utf8");
}

console.log(`Created ${datasets.length} deterministic CSV datasets in ${outputDir}`);
