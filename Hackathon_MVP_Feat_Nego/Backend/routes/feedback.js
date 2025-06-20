// server/src/routes/feedback.js
const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const multer = require('multer');
const router = express.Router();

// Configure multer for file uploads
// We'll use memory storage for simplicity, but for larger files, disk storage is better.
const storage = multer.memoryStorage();
const upload = multer({
    storage: storage,
    limits: { fileSize: 10 * 1024 * 1024 }, // 10MB limit
    fileFilter: (req, file, cb) => {
        const isJsonMimeType = file.mimetype === 'application/json';
        // Ensure case-insensitive check for extension, consistent with frontend
        const isJsonExtension = file.originalname.toLowerCase().endsWith('.json');

        if (isJsonMimeType || isJsonExtension) {
            cb(null, true);
        } else {
            cb(new Error('Only .json files are allowed!'), false);
        }
    }
});

// Define a directory for temporary files
const TEMP_DIR = path.join(__dirname, '../input_features.json');

// Ensure the temporary directory exists
fs.mkdir(TEMP_DIR, { recursive: true }).catch(console.error);

router.post('/upload', upload.single('feedback'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ success: false, error: 'No file uploaded or invalid file type.' });
    }

    const pythonScriptPath = path.join(__dirname, '../python/main.py');
    const uniqueId = Date.now() + '-' + Math.random().toString(36).substring(2, 9);
    const tempInputFilename = `input_${uniqueId}.json`;
    const tempOutputFilename = `output_${uniqueId}.json`;
    const tempInputPath = path.join(TEMP_DIR, tempInputFilename);
    const tempOutputPath = path.join(TEMP_DIR, tempOutputFilename);

    try {
        // Validate JSON content from buffer before writing
        const fileContent = req.file.buffer.toString('utf8');
        let jsonData;
        try {
            jsonData = JSON.parse(fileContent);
        } catch (parseError) {
            console.error('Invalid JSON format in uploaded file:', parseError);
            return res.status(400).json({
                success: false,
                error: 'Invalid JSON format in uploaded file'
            });
        }

        // Save uploaded file content to a temporary input file for the Python script
        await fs.writeFile(tempInputPath, fileContent, 'utf8');

        const pythonProcess = spawn('python3', [pythonScriptPath, tempInputPath, tempOutputPath]);

        let stdoutData = '';
        let stderrData = '';

        pythonProcess.stdout.on('data', (data) => {
            stdoutData += data.toString();
            console.log(`Python stdout: ${data}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            stderrData += data.toString();
            console.error(`Python stderr: ${data}`);
        });

        pythonProcess.on('close', async (code) => {
            console.log(`Python script exited with code ${code}`);

            if (code === 0) {
                try {
                    // Read the output file created by the Python script
                    const resultData = await fs.readFile(tempOutputPath, 'utf8');
                    const resultJson = JSON.parse(resultData);

                    res.json({
                        success: true,
                        message: 'File uploaded and processed successfully',
                        data: {
                            filename: req.file.originalname,
                            size: req.file.size,
                            pythonResult: resultJson
                        }
                    });
                } catch (parseOrReadError) {
                    console.error("Error reading/parsing Python script output file:", parseOrReadError);
                    res.status(500).json({ success: false, error: 'Failed to read or parse Python script output', details: parseOrReadError.message, stderr: stderrData });
                }
            } else {
                res.status(500).json({ success: false, error: `Python script execution failed with code ${code}`, stderr: stderrData });
            }

            // Cleanup temporary files
            try {
                await fs.unlink(tempInputPath);
                await fs.unlink(tempOutputPath);
            } catch (cleanupError) {
                console.error("Error cleaning up temporary files:", cleanupError);
            }
        });

        pythonProcess.on('error', (err) => {
            console.error('Failed to start Python subprocess.', err);
            res.status(500).json({ success: false, error: 'Failed to start Python script process', details: err.message });
            // No need to cleanup here as files might not have been created or spawn failed.
        });
    } catch (error) {
        console.error('Error in /upload route:', error);
        res.status(500).json({
            success: false,
            error: 'An unexpected error occurred during file processing.',
            details: error.message
        });
        // Attempt to cleanup files even on outer error
        try {
            if (await fs.stat(tempInputPath).catch(() => false)) await fs.unlink(tempInputPath);
            if (await fs.stat(tempOutputPath).catch(() => false)) await fs.unlink(tempOutputPath);
        } catch (cleanupError) {
            console.error("Error cleaning up temporary files on failure:", cleanupError);
        }
    }
});

router.get('/results', async (req, res, next) => {
    try {
        const taxonomyFilePath = path.join(__dirname, '../python/feedback_taxonomy.json');
        const taxonomyContent = await fs.readFile(taxonomyFilePath, 'utf8');
        res.json(JSON.parse(taxonomyContent));
    } catch (err) {
        console.error("Error reading taxonomy file in /results:", err);
        next(err);
    }
});

module.exports = router;