const express = require("express");
const multer = require("multer");
const Redis = require("ioredis");
const fs = require("fs");
const path = require("path");

const app = express();
const redisUrl = process.env.REDIS_URL || "redis://redis_db:6379";
const redis = new Redis(redisUrl);

app.use(express.static("public"));

// Configure Multer to save files to the '/app/uploads' folder inside the container
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Ensure directory exists
    if (!fs.existsSync("/app/uploads")) {
      fs.mkdirSync("/app/uploads");
    }
    cb(null, "/app/uploads");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

const upload = multer({ storage: storage });

app.post("/upload", upload.single("image"), async (req, res) => {
  const file = req.file;
  
  // 1. Log that we got the file
  console.log(`Received file: ${file.filename}`);

  // 2. Send a message to Redis (The Queue)
  // We push a JSON string containing the filename so the worker knows what to process
  await redis.lpush("task_queue", JSON.stringify({ filename: file.filename }));

  // 3. Respond to user immediately
  res.json({ message: "File uploaded! Processing started.", filename: file.filename });
});

app.listen(3000, () => {
  console.log("API Service running on port 3000");
});