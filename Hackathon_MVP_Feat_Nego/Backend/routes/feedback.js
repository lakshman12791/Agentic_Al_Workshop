// server/src/routes/feedback.js
const express = require('express');
const { exec, spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const multer = require('multer');
const router = express.Router();


async function processJsonData(jsonData) {
    try {
        let summary = {
            totalRecords: 0,
            processedAt: new Date().toISOString()
        };

        if (Array.isArray(jsonData)) {
            summary.totalRecords = jsonData.length;
            summary.type = 'array';

            jsonData.forEach((item, index) => {
                console.log(`Processing record ${index + 1}:`, Object.keys(item));
            });

        } else if (typeof jsonData === 'object') {
            summary.totalRecords = 1;
            summary.type = 'object';
            summary.fields = Object.keys(jsonData);

        }
        return {
            success: true,
            summary: summary
        };

    } catch (error) {
        console.error('Data processing error:', error);
        throw new Error('Failed to process JSON data');
    }
}


router.post('/upload', express.json({ limit: '10mb' }), async (req, res) => {
    try {

        const UPLOAD_DIR = path.join(__dirname, '../python');

        const fileContent = req.file.buffer.toString('utf8');

        let jsonData;
        try {
            jsonData = JSON.parse(fileContent);
        } catch (parseError) {
            return res.status(400).json({
                success: false,
                error: 'Invalid JSON format in uploaded file'
            });
        }

        const processedData = await processJsonData(jsonData);
        const filePath = path.join(UPLOAD_DIR, "feedback_taxonomy.json");

        // Save file to disk
        await fs.writeFile(filePath, fileContent, 'utf8');

        const python = spawn('python', ['python/feedback_analyzer.py']);

        python.stdout.on('data', (data) => {
            console.log(`Output: ${data}`);
        });

        python.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);
        });

        python.on('close', (code) => {
            console.log(`Process exited with code ${code}`);
        });




        // res.json({
        //     success: true,
        //     message: 'File uploaded and processed successfully',
        //     data: {
        //         filename: req.file.originalname,
        //         size: req.file.size,
        //         recordsProcessed: Array.isArray(jsonData) ? jsonData.length : 1,
        //         summary: processedData.summary
        //     }
        // });

    } catch (error) {
        console.error('Save error:', error);
        res.status(500).json({
            error: 'Failed to save JSON data',
            details: error.message
        });
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