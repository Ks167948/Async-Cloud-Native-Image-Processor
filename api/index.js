const express = require("express");
const multer = require("multer");
const multerS3 = require("multer-s3");
const { S3Client } = require("@aws-sdk/client-s3");
const Redis = require("ioredis");
const path = require("path");

const app = express();

// 1. Configure AWS S3
const s3 = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

// 2. Configure Redis (Cloud or Local)
const redisUrl = process.env.REDIS_URL || "redis://redis_db:6379";
const redis = new Redis(redisUrl);

// 3. Configure Multer to upload directly to S3
const upload = multer({
  storage: multerS3({
    s3: s3,
    bucket: process.env.AWS_BUCKET_NAME,
    metadata: function (req, file, cb) {
      cb(null, { fieldName: file.fieldname });
    },
    key: function (req, file, cb) {
      // Save file as "uploads/timestamp-filename"
      cb(null, `uploads/${Date.now().toString()}-${file.originalname}`);
    },
  }),
});

app.use(express.static("public"));

app.post("/upload", upload.single("image"), async (req, res) => {
  // Multer-S3 adds a 'location' property to the file object with the S3 URL
  const file = req.file;
  console.log(`Uploaded to S3: ${file.location}`);

  // Push the S3 Key (filename) to Redis so the worker knows what to download
  await redis.lpush("task_queue", JSON.stringify({ 
    key: file.key,        // The filename in S3
    url: file.location    // The public URL
  }));

  res.json({ message: "Uploaded to S3! Processing started.", url: file.location });
});

app.listen(3000, () => console.log("API Service running on port 3000"));