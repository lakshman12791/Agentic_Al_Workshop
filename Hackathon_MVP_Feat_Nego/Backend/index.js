const express = require("express");
const multer = require("multer");
const { GoogleGenerativeAI } = require("@google/generative-ai");
const app = express();
const port = process.env.PORT || 3001;
const cors = require('cors');

const GEMINI_API_KEY = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo";
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const feedbackRoutes = require('./routes/feedback');
const errorHandler = require('./middleware/errorHandler');

app.use(cors());
app.use(express.json());
app.use('/api/feedback-parser', upload.single('feedback'), feedbackRoutes);
app.use(errorHandler);



app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});