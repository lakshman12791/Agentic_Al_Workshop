// server/src/routes/feedback.js
const express = require('express');
const { exec } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

const router = express.Router();

router.post('/upload', async (req, res, next) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        const inputPath = req.file.path;
        const outputPath = path.join(__dirname, '../../Backend/python/feedback_taxonomy.json');

        // Run Python RAG parser
        exec(
            `python3 ${path.join(__dirname, '../../Backend/python/rag_parser.py')} ${inputPath} ${outputPath}`,
            async (err) => {
                if (err) {
                    return next(err);
                }

                try {
                    const results = await fs.readFile(outputPath, 'utf8');
                    res.json(JSON.parse(results));
                } catch (readErr) {
                    next(readErr);
                }
            }
        );
    } catch (err) {
        next(err);
    }
});

router.get('/results', async (req, res, next) => {
    try {
        const outputPath = path.join(__dirname, '../../Backend/python/feedback_taxonomy.json');
        const results = await fs.readFile(outputPath, 'utf8');
        res.json(JSON.parse(results));
    } catch (err) {
        console.log("err", err)
        next(err);
    }
});

module.exports = router;