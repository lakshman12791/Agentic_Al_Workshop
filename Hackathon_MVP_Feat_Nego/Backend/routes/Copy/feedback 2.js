// server/src/routes/feedback.js
const express = require('express');
const { exec, spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const multer = require('multer');
const router = express.Router();


// const storage = multer.memoryStorage();

// const upload = multer({ storage: storage });

// router.post('/upload', async (req, res, next) => {
// router.post('/upload', upload.single('feedback'), async (req, res, next) => {

//     try {

//         console.log("feedback", feedback)

//         if (!req.file) {
//             return res.status(400).json({ error: 'No file uploaded' });
//         }

//         const inputPath = req.file.path;
//         const outputPath = path.join(__dirname, '../../Backend/python/feedback_taxonomy.json');

//         console.log("inputPath", inputPath)
//         console.log("outputPath", outputPath)


//         // Run Python RAG parser
//         exec(
//             `python3 ${path.join(__dirname, '../../Backend/python/rag_parser.py')} ${inputPath} ${outputPath}`,
//             async (err) => {
//                 if (err) {
//                     return next(err);
//                 }

//                 try {
//                     const results = await fs.readFile(outputPath, 'utf8');
//                     res.json(JSON.parse(results));
//                 } catch (readErr) {
//                     next(readErr);
//                 }
//             }
//         );
//     } catch (err) {
//         console.log("err", err)

//         next(err);
//     }
// });



// router.post('/upload', async (req, res, next) => {

//     try {

//         console.log("req", req)

//         if (!req.file) {
//             return res.status(400).json({ error: 'No file uploaded' });
//         }

//         const inputPath = req.file.path;
//         const outputPath = path.join(__dirname, '../../Backend/python/feedback_taxonomy.json');

//         console.log("inputPath", inputPath)
//         console.log("outputPath", outputPath)


//         // Run Python RAG parser
//         exec(
//             `python3 ${path.join(__dirname, '../../Backend/python/rag_parser.py')} ${inputPath} ${outputPath}`,
//             async (err) => {
//                 if (err) {
//                     return next(err);
//                 }

//                 try {
//                     const results = await fs.readFile(outputPath, 'utf8');
//                     res.json(JSON.parse(results));
//                 } catch (readErr) {
//                     next(readErr);
//                 }
//             }
//         );
//     } catch (err) {
//         console.log("err", err)

//         next(err);
//     }
// });


// const storage = multer.diskStorage({
//     destination: function (req, file, cb) {
//         // Use temp directory for initial upload
//         const tempDir = os.tmpdir();
//         cb(null, tempDir);
//     },
//     filename: function (req, file, cb) {
//         // Generate unique filename
//         const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
//         cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
//     }
// });

// File filter to accept only JSON files
// const fileFilter = (req, file, cb) => {
//     if (file.mimetype === 'application/json' || path.extname(file.originalname).toLowerCase() === '.json') {
//         cb(null, true);
//     } else {
//         cb(new Error('Only JSON files are allowed!'), false);
//     }
// };

// const upload = multer({
//     storage: storage,
//     fileFilter: fileFilter,
//     limits: {
//         fileSize: 10 * 1024 * 1024 // 10MB limit
//     }
// });

// Method 1: Upload JSON file using multipart/form-data
// router.post('/upload', upload.single('feedback'), async (req, res) => {
//     try {
//         if (!req.file) {
//             return res.status(400).json({ error: 'No JSON file uploaded' });
//         }

//         console.log('Uploaded file:', req.file);

//         // Define backend storage path (adjust as needed)
//         const backendDir = path.join(__dirname, '../data/uploads');

//         // Ensure directory exists
//         await fs.mkdir(backendDir, { recursive: true });

//         // Create final file path
//         const finalFileName = `uploaded-${Date.now()}.json`;
//         const finalPath = path.join(backendDir, finalFileName);

//         // Read the uploaded file
//         const fileContent = await fs.readFile(req.file.path, 'utf8');

//         // Validate JSON format
//         let jsonData;
//         try {
//             jsonData = JSON.parse(fileContent);
//         } catch (parseError) {
//             // Clean up temp file
//             await fs.unlink(req.file.path);
//             return res.status(400).json({
//                 error: 'Invalid JSON format',
//                 details: parseError.message
//             });
//         }

//         // Save to final location with pretty formatting
//         await fs.writeFile(finalPath, JSON.stringify(jsonData, null, 2), 'utf8');

//         // Clean up temporary file
//         await fs.unlink(req.file.path);

//         console.log('JSON file saved to:', finalPath);

//         res.json({
//             message: 'JSON file uploaded and saved successfully',
//             fileName: finalFileName,
//             filePath: finalPath,
//             fileSize: req.file.size,
//             recordCount: Array.isArray(jsonData) ? jsonData.length : Object.keys(jsonData).length
//         });

//     } catch (error) {
//         console.error('Upload error:', error);

//         // Clean up temp file if it exists
//         if (req.file && req.file.path) {
//             try {
//                 await fs.unlink(req.file.path);
//             } catch (cleanupError) {
//                 console.error('Cleanup error:', cleanupError);
//             }
//         }

//         res.status(500).json({
//             error: 'Failed to upload JSON file',
//             details: error.message
//         });
//     }
// });

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