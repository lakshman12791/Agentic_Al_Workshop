import React, { useState, useEffect } from 'react';

function FeedbackResults() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchResults = async () => {
            setLoading(true);
            try {
                const response = await fetch('http://localhost:3001/api/feedback/results');
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
                                <td className="border p-2">{result.desirability_score}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No results available</p>
            )}
        </div>
    );
}

export default FeedbackResults;