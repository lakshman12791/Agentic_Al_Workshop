// import React, { useState } from 'react';

// function FeedbackUploader() {
//   const [file, setFile] = useState(null);
//   const [uploading, setUploading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//     setError(null);
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       setError('Please select a file');
//       return;
//     }

//     setUploading(true);
//     const formData = new FormData();
//     formData.append('feedback', file);

//     try {
//       const response = await fetch('http://localhost:3001/api/feedback/upload', {
//         method: 'POST',
//         body: formData,
//       });

//       if (!response.ok) {
//         throw new Error('Upload failed');
//       }

//       const data = await response.json();
//       console.log('Upload success:', data);
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setUploading(false);
//     }
//   };

//   return (
//     <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
//       <h2 className="text-xl font-semibold mb-4">Upload Feedback</h2>
//       <input
//         type="file"
//         accept=".txt,.csv,.json"
//         onChange={handleFileChange}
//         className="mb-4"
//       />
//       <button
//         onClick={handleUpload}
//         disabled={uploading}
//         className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
//       >
//         {uploading ? 'Uploading...' : 'Upload'}
//       </button>
//       {error && <p className="text-red-500 mt-2">{error}</p>}
//     </div>
//   );
// }

// export default FeedbackUploader;

// -----------------------------------------------------------------------------------------------------

// import React, { useState } from 'react';
// import { Upload, FileText, CheckCircle, AlertCircle, Cloud } from 'lucide-react';

// export default function UploadFeedbackUI() {
//   const [file, setFile] = useState(null);
//   const [uploading, setUploading] = useState(false);
//   const [uploaded, setUploaded] = useState(false);
//   const [error, setError] = useState('');
//   const [dragActive, setDragActive] = useState(false);

//   const handleFileChange = (e) => {
//     const selectedFile = e.target.files[0];
//     if (selectedFile) {
//       setFile(selectedFile);
//       setError('');
//       setUploaded(false);
//     }
//   };

//   const handleDrag = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     if (e.type === "dragenter" || e.type === "dragover") {
//       setDragActive(true);
//     } else if (e.type === "dragleave") {
//       setDragActive(false);
//     }
//   };

//   const handleDrop = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     setDragActive(false);
    
//     if (e.dataTransfer.files && e.dataTransfer.files[0]) {
//       const droppedFile = e.dataTransfer.files[0];
//       const allowedTypes = ['.txt', '.csv', '.json'];
//       const fileExtension = '.' + droppedFile.name.split('.').pop().toLowerCase();
      
//       if (allowedTypes.includes(fileExtension)) {
//         setFile(droppedFile);
//         setError('');
//         setUploaded(false);
//       } else {
//         setError('Please upload a .txt, .csv, or .json file');
//       }
//     }
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       setError('Please select a file first');
//       return;
//     }

//     setUploading(true);
//     setError('');
    
//     // Simulate upload process
//     try {
//       await new Promise(resolve => setTimeout(resolve, 2000));
//       setUploaded(true);
//       setUploading(false);
//     } catch (err) {
//       setError('Upload failed. Please try again.');
//       setUploading(false);
//     }
//   };

//   const formatFileSize = (bytes) => {
//     if (bytes === 0) return '0 Bytes';
//     const k = 1024;
//     const sizes = ['Bytes', 'KB', 'MB', 'GB'];
//     const i = Math.floor(Math.log(bytes) / Math.log(k));
//     return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
//   };

//   const getFileIcon = (fileName) => {
//     const extension = fileName.split('.').pop().toLowerCase();
//     return <FileText className="w-8 h-8 text-blue-500" />;
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center p-4">
//       <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-2xl w-full max-w-lg border border-white/20">
//         {/* Header */}
//         <div className="text-center mb-8">
//           <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mb-4 shadow-lg">
//             <Cloud className="w-8 h-8 text-white" />
//           </div>
//           <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent mb-2">
//             Upload Feedback
//           </h2>
//           <p className="text-gray-600">Share your feedback files with us</p>
//         </div>

//         {/* Upload Area */}
//         <div
//           className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
//             dragActive
//               ? 'border-blue-500 bg-blue-50/50 scale-105'
//               : uploaded
//               ? 'border-green-500 bg-green-50/50'
//               : error
//               ? 'border-red-500 bg-red-50/50'
//               : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50/30'
//           }`}
//           onDragEnter={handleDrag}
//           onDragLeave={handleDrag}
//           onDragOver={handleDrag}
//           onDrop={handleDrop}
//         >
//           <input
//             type="file"
//             accept=".txt,.csv,.json"
//             onChange={handleFileChange}
//             className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
//             id="file-upload"
//           />
          
//           <div className="space-y-4">
//             {uploaded ? (
//               <CheckCircle className="w-16 h-16 text-green-500 mx-auto animate-pulse" />
//             ) : (
//               <Upload className={`w-16 h-16 mx-auto transition-colors duration-300 ${
//                 dragActive ? 'text-blue-500' : 'text-gray-400'
//               }`} />
//             )}
            
//             <div>
//               {uploaded ? (
//                 <p className="text-green-600 font-semibold text-lg">File uploaded successfully!</p>
//               ) : (
//                 <>
//                   <p className="text-gray-700 font-medium text-lg mb-2">
//                     {dragActive ? 'Drop your file here' : 'Drag & drop your file here'}
//                   </p>
//                   <p className="text-gray-500 text-sm">
//                     or <span className="text-blue-600 font-medium">browse</span> to choose a file
//                   </p>
//                 </>
//               )}
//             </div>
            
//             <div className="flex justify-center space-x-4 text-xs text-gray-500">
//               <span className="bg-gray-100 px-2 py-1 rounded">.txt</span>
//               <span className="bg-gray-100 px-2 py-1 rounded">.csv</span>
//               <span className="bg-gray-100 px-2 py-1 rounded">.json</span>
//             </div>
//           </div>
//         </div>

//         {/* File Info */}
//         {file && !uploaded && (
//           <div className="mt-6 p-4 bg-gray-50 rounded-xl border border-gray-200">
//             <div className="flex items-center space-x-3">
//               {getFileIcon(file.name)}
//               <div className="flex-1 min-w-0">
//                 <p className="text-sm font-medium text-gray-900 truncate">{file.name}</p>
//                 <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
//               </div>
//             </div>
//           </div>
//         )}

//         {/* Upload Button */}
//         <button
//           onClick={handleUpload}
//           disabled={uploading || !file || uploaded}
//           className={`w-full mt-6 px-6 py-4 rounded-xl font-semibold text-white transition-all duration-300 transform ${
//             uploading
//               ? 'bg-gray-400 cursor-not-allowed'
//               : uploaded
//               ? 'bg-green-500 hover:bg-green-600'
//               : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:scale-105 shadow-lg hover:shadow-xl'
//           }`}
//         >
//           <div className="flex items-center justify-center space-x-2">
//             {uploading ? (
//               <>
//                 <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
//                 <span>Uploading...</span>
//               </>
//             ) : uploaded ? (
//               <>
//                 <CheckCircle className="w-5 h-5" />
//                 <span>Uploaded Successfully</span>
//               </>
//             ) : (
//               <>
//                 <Upload className="w-5 h-5" />
//                 <span>Upload File</span>
//               </>
//             )}
//           </div>
//         </button>

//         {/* Error Message */}
//         {error && (
//           <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl">
//             <div className="flex items-center space-x-2">
//               <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
//               <p className="text-red-700 text-sm font-medium">{error}</p>
//             </div>
//           </div>
//         )}

//         {/* Footer */}
//         <div className="mt-8 text-center">
//           <p className="text-xs text-gray-500">
//             Maximum file size: 10MB • Supported formats: TXT, CSV, JSON
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// }


// ----------------------------------------------------------------------------------------------------------------

// import React, { useState } from 'react';
// import { Upload, FileText, CheckCircle, AlertCircle, Cloud } from 'lucide-react';
// import '../index.css'; 
// import '../app.css'; 


// export default function UploadFeedbackUI() {
//   const [file, setFile] = useState(null);
//   const [uploading, setUploading] = useState(false);
//   const [uploaded, setUploaded] = useState(false);
//   const [error, setError] = useState('');
//   const [dragActive, setDragActive] = useState(false);

//   const handleFileChange = (e) => {
//     const selectedFile = e.target.files[0];
//     if (selectedFile) {
//       setFile(selectedFile);
//       setError('');
//       setUploaded(false);
//     }
//   };

//   const handleDrag = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     setDragActive(e.type === 'dragenter' || e.type === 'dragover');
//   };

//   const handleDrop = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     setDragActive(false);

//     if (e.dataTransfer.files && e.dataTransfer.files[0]) {
//       const droppedFile = e.dataTransfer.files[0];
//       const allowedTypes = ['.txt', '.csv', '.json'];
//       const fileExtension = '.' + droppedFile.name.split('.').pop().toLowerCase();

//       if (allowedTypes.includes(fileExtension)) {
//         setFile(droppedFile);
//         setError('');
//         setUploaded(false);
//       } else {
//         setError('Please upload a .txt, .csv, or .json file');
//       }
//     }
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       setError('Please select a file first');
//       return;
//     }

//     setUploading(true);
//     setError('');
//     try {
//       await new Promise((resolve) => setTimeout(resolve, 2000));
//       setUploaded(true);
//     } catch {
//       setError('Upload failed. Please try again.');
//     } finally {
//       setUploading(false);
//     }
//   };

//   const formatFileSize = (bytes) => {
//     if (bytes === 0) return '0 Bytes';
//     const k = 1024;
//     const sizes = ['Bytes', 'KB', 'MB', 'GB'];
//     const i = Math.floor(Math.log(bytes) / Math.log(k));
//     return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center p-4">
//       <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-2xl w-full max-w-lg border border-white/20">
//         {/* Header */}
//         <div className="text-center mb-8">
//           <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mb-4 shadow-lg">
//             <Cloud className="w-8 h-8 text-white" />
//           </div>
//           <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent mb-2">
//             Upload Feedback
//           </h2>
//           <p className="text-gray-600">Share your feedback files with us</p>
//         </div>

//         {/* Upload Area */}
//         <div
//           className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
//             dragActive
//               ? 'border-blue-500 bg-blue-50/50 scale-105'
//               : uploaded
//               ? 'border-green-500 bg-green-50/50'
//               : error
//               ? 'border-red-500 bg-red-50/50'
//               : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50/30'
//           }`}
//           onDragEnter={handleDrag}
//           onDragLeave={handleDrag}
//           onDragOver={handleDrag}
//           onDrop={handleDrop}
//         >
//           <input
//             id="file-upload"
//             type="file"
//             accept=".txt,.csv,.json"
//             onChange={handleFileChange}
//             className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
//           />
//           <label htmlFor="file-upload" className="block space-y-4 cursor-pointer">
//             {uploaded ? (
//               <CheckCircle className="w-16 h-16 text-green-500 mx-auto animate-pulse" />
//             ) : (
//               <Upload
//                 className={`w-16 h-16 mx-auto transition-colors duration-300 ${
//                   dragActive ? 'text-blue-500' : 'text-gray-400'
//                 }`}
//               />
//             )}
//             <div>
//               {uploaded ? (
//                 <p className="text-green-600 font-semibold text-lg">File uploaded successfully!</p>
//               ) : (
//                 <>
//                   <p className="text-gray-700 font-medium text-lg mb-2">
//                     {dragActive ? 'Drop your file here' : 'Drag & drop your file here'}
//                   </p>
//                   <p className="text-gray-500 text-sm">
//                     or <span className="text-blue-600 font-medium">browse</span> to choose a file
//                   </p>
//                 </>
//               )}
//             </div>
//             <div className="flex justify-center gap-2 text-xs text-gray-500">
//               {['.txt', '.csv', '.json'].map((ext) => (
//                 <span key={ext} className="bg-gray-100 px-2 py-1 rounded">
//                   {ext}
//                 </span>
//               ))}
//             </div>
//           </label>
//         </div>

//         {/* File Info */}
//         {file && !uploaded && (
//           <div className="mt-6 p-4 bg-gray-50 rounded-xl border border-gray-200">
//             <div className="flex items-center gap-3">
//               <FileText className="w-8 h-8 text-blue-500" />
//               <div className="flex-1 min-w-0">
//                 <p className="text-sm font-medium text-gray-900 truncate">{file.name}</p>
//                 <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
//               </div>
//             </div>
//           </div>
//         )}

//         {/* Upload Button */}
//         <button
//           onClick={handleUpload}
//           disabled={uploading || !file || uploaded}
//           className={`w-full mt-6 px-6 py-4 rounded-xl font-semibold text-white transition-all duration-300 transform ${
//             uploading
//               ? 'bg-gray-400 cursor-not-allowed'
//               : uploaded
//               ? 'bg-green-500 hover:bg-green-600'
//               : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:scale-105 shadow-lg hover:shadow-xl'
//           }`}
//         >
//           <div className="flex items-center justify-center gap-2">
//             {uploading ? (
//               <>
//                 <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
//                 <span>Uploading...</span>
//               </>
//             ) : uploaded ? (
//               <>
//                 <CheckCircle className="w-5 h-5" />
//                 <span>Uploaded Successfully</span>
//               </>
//             ) : (
//               <>
//                 <Upload className="w-5 h-5" />
//                 <span>Upload File</span>
//               </>
//             )}
//           </div>
//         </button>

//         {/* Error Message */}
//         {error && (
//           <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl">
//             <div className="flex items-center gap-2">
//               <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
//               <p className="text-red-700 text-sm font-medium">{error}</p>
//             </div>
//           </div>
//         )}

//         {/* Footer */}
//         <p className="mt-8 text-center text-xs text-gray-500">
//           Maximum file size: 10MB • Supported formats: TXT, CSV, JSON
//         </p>
//       </div>
//     </div>
//   );
// }


// -------------------------------------------------------------------------------------------------------------------

import React, { useState } from 'react';

function FeedbackUploader() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('feedback', file);

    try {
      const response = await fetch('http://localhost:3001/api/feedback/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      console.log('Upload success:', data);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
      <h2 className="text-xl font-semibold mb-4">Upload Feedback</h2>
      <input
        type="file"
        accept=".txt,.csv,.json"
        onChange={handleFileChange}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        disabled={uploading}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}

export default FeedbackUploader;