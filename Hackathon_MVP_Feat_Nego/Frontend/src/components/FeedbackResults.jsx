// import React, { useState, useEffect } from 'react';

// export default function DesirabilityTag({ desirability_score }) {
//     let tagLabel = '';
//     let tagStyle = '';

//     if (desirability_score < 4) {
//         tagLabel = 'No usage';
//         tagStyle = 'bg-red-100 text-red-700 border border-red-300';
//     } else if (desirability_score >= 4 && desirability_score < 7) {
//         tagLabel = 'Moderate usage';
//         tagStyle = 'bg-yellow-100 text-yellow-800 border border-yellow-300';
//     } else if (desirability_score >= 8) {
//         tagLabel = 'Frequent usage';
//         tagStyle = 'bg-green-100 text-green-800 border border-green-300';
//     } else {
//         tagLabel = 'Unknown';
//         tagStyle = 'bg-gray-100 text-gray-600 border border-gray-300';
//     }

//     return (
//         <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${tagStyle}`}>
//             {tagLabel}
//         </span>
//     );
// }

// function FeedbackResults() {
//     const [results, setResults] = useState([]);
//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState(null);

//     useEffect(() => {
//         const fetchResults = async () => {
//             setLoading(true);
//             try {
//                 const response = await fetch('http://localhost:3001/api/feedback-parser/results');
//                 if (!response.ok) {
//                     throw new Error('Failed to fetch results');
//                 }
//                 const data = await response.json();
//                 setResults(data);
//             } catch (err) {
//                 setError(err.message);
//             } finally {
//                 setLoading(false);
//             }
//         };

//         fetchResults();
//     }, []);

//     return (
//         <div className="mt-8 w-full max-w-4xl">
//             <h2 className="text-xl font-semibold mb-4">Parsed Feedback Results</h2>
//             {loading && <p>Loading...</p>}
//             {error && <p className="text-red-500">{error}</p>}
//             {results.length > 0 ? (
//                 <table className="w-full border-collapse border">
//                     <thead>
//                         <tr className="bg-gray-200">
//                             <th className="border p-2">Feature</th>
//                             <th className="border p-2">Need</th>
//                             <th className="border p-2">Desirability Score</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         {results.map((result, index) => (
//                             <tr key={index}>
//                                 <td className="border p-2">{result.feature}</td>
//                                 <td className="border p-2">{result.need}</td>
//                                 <td className="border p-2">
//                                     <DesirabilityTag desirability_score={result.desirability_score} />
//                                 </td>
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//             ) : (
//                 <p>No results available</p>
//             )}
//         </div>
//     );
// }

// export default FeedbackResults;

import React, { useState, useEffect } from 'react';

export function DesirabilityTag({ desirability_score }) {
    let tagLabel = '';
    let tagStyle = '';

    console.log("desirability_score", desirability_score)

    if (desirability_score < 4) {
        tagLabel = 'No usage';
        tagStyle = 'bg-red-100 text-red-700 border border-red-300';
    } else if (desirability_score >= 4 && desirability_score <= 7) {
        tagLabel = 'Moderate usage';
        tagStyle = 'bg-yellow-100 text-yellow-800 border border-yellow-300';
    } else if (desirability_score > 7) {
        tagLabel = 'Frequent usage';
        tagStyle = 'bg-green-100 text-green-800 border border-green-300';
    } else {
        tagLabel = 'Unknown';
        tagStyle = 'bg-gray-100 text-gray-600 border border-gray-300';
    }

    return (
        <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${tagStyle}`}>
            {tagLabel}
        </span>
    );
}

function FeedbackResults() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchResults = async () => {
            setLoading(true);
            try {
                const response = await fetch('http://localhost:3001/api/feedback-parser/results');
                if (!response.ok) {
                    throw new Error('Failed to fetch results');
                }
                const data = await response.json();
                setResults(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchResults();
    }, []);

    return (
        <div className="mt-8 w-full max-w-4xl">
            <h2 className="text-xl font-semibold mb-4">Parsed Feedback Results</h2>
            {loading && <p>Loading...</p>}
            {error && <p className="text-red-500">{error}</p>}
            {results.length > 0 ? (
                <table className="w-full border-collapse border">
                    <thead>
                        <tr className="bg-gray-200">
                            <th className="border p-2">Feature</th>
                            <th className="border p-2">Need</th>
                            <th className="border p-2">Desirability Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {results.map((result, index) => (
                            <tr key={index}>
                                <td className="border p-2">{result.feature}</td>
                                <td className="border p-2">{result.need}</td>
                                <td className="border p-2">
                                    <DesirabilityTag desirability_score={result.desirability_score} />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                !loading && <p>No results available</p>
            )}
        </div>
    );
}

export default FeedbackResults;
