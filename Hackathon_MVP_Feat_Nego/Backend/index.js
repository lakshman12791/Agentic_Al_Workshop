const express = require("express");
const multer = require("multer");
const { GoogleGenerativeAI } = require("@google/generative-ai");
const app = express();
const port = process.env.PORT || 3000;

const GEMINI_API_KEY = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo";
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.post("/mvp-feature-negotiator-agent/feedback-parser", upload.single("document"), async (req, res) => {
    try {
        if (!req.file) return res.status(400).json({ error: "No file uploaded" });
        // const result = await processImage(req.file, PROMPTS.COMMUNITY);
        // res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});