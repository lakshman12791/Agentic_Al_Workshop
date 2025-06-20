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
    let tagStyle = {};

    console.log("desirability_score", desirability_score);

    if (desirability_score < 4) {
        tagLabel = 'No usage';
        tagStyle = {
            backgroundColor: '#fee2e2', // red-100
            color: '#b91c1c',           // red-700
            border: '1px solid #fca5a5' // red-300
        };
    } else if (desirability_score >= 4 && desirability_score <= 7) {
        tagLabel = 'Moderate usage';
        tagStyle = {
            backgroundColor: '#fef9c3', // yellow-100
            color: '#92400e',           // yellow-800
            border: '1px solid #fde68a' // yellow-300
        };
    } else if (desirability_score > 7) {
        tagLabel = 'Frequent usage';
        tagStyle = {
            backgroundColor: '#d1fae5', // green-100
            color: '#065f46',           // green-800
            border: '1px solid #6ee7b7' // green-300
        };
    } else {
        tagLabel = 'Unknown';
        tagStyle = {
            backgroundColor: '#f3f4f6', // gray-100
            color: '#4b5563',           // gray-600
            border: '1px solid #d1d5db' // gray-300
        };
    }

    return (
        <span
            style={{
                display: 'inline-block',
                padding: '0.25rem 0.75rem',
                borderRadius: '9999px',
                fontSize: '0.875rem',
                fontWeight: 500,
                ...tagStyle
            }}
        >
            {tagLabel}
        </span>
    );
}


// export function DesirabilityTag({ desirability_score }) {
//     let tagLabel = '';
//     let tagStyle = '';

//     console.log("desirability_score", desirability_score)

//     if (desirability_score < 4) {
//         tagLabel = 'No usage';
//         tagStyle = 'bg-red-100 text-red-700 border border-red-300';
//     } else if (desirability_score >= 4 && desirability_score <= 7) {
//         tagLabel = 'Moderate usage';
//         tagStyle = 'bg-yellow-100 text-yellow-800 border border-yellow-300';
//     } else if (desirability_score > 7) {
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

    const thStyle = {
    border: '1px solid #ccc',
    padding: '0.5rem',
    textAlign: 'left',
    fontWeight: 'bold',
    backgroundColor: '#f3f4f6'
};

const tdStyle = {
    border: '1px solid #ccc',
    padding: '0.5rem',
    verticalAlign: 'top'
};

    return (
        <div style={{ marginTop: '2rem', width: '100%', maxWidth: '64rem' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1rem' }}>
                Parsed Feedback Results
            </h2>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: '#ef4444' }}>{error}</p>}

            {results.length > 0 ? (
                <table
                    style={{
                        width: '100%',
                        borderCollapse: 'collapse',
                        border: '1px solid #ccc'
                    }}
                >
                    <thead>
                        <tr style={{ backgroundColor: '#e5e7eb' }}>
                            <th style={thStyle}>Feature</th>
                            <th style={thStyle}>Need</th>
                            <th style={thStyle}>Desirability Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {results.map((result, index) => (
                            <tr key={index}>
                                <td style={tdStyle}>{result.feature}</td>
                                <td style={tdStyle}>{result.need}</td>
                                <td style={tdStyle}>
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
