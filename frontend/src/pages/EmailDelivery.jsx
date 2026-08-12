import {useEffect, useState} from 'react';
import API from '../api/axios';
import Navbar from "../components/navbar";

function EmailDelivery(){
    const[data, setData] = useState(null);
    const[loading, setLoading] = useState(true);
    const[error, setError] = useState(null);

    useEffect(() => {
        API.get('emails/log/')
           .then((res) => setData(res.data))
           .catch((err) => setError(err.response?.data?.error || "Failed to load email log"))
           .finally(() => setLoading(false))
    }, []);

    if(loading) return (
        <>
        <Navbar />
            <div className='flex justify-center items-center h-64 text-gray-500'>
            Loading...
            </div>
        </>
    )
    if(error) return(
        <>
        <Navbar />
        <div className='max-w-2xl mx-auto mt-16 text-center text-red-600 font-semibold'>
            {error}
        </div>
        </>
    )

    const {delivery_rate, total, sent, failed, queued, logs} = data;

    // arrow function badge('sent')
    const badge = (s) => {
        const map = { // js object
            sent: "bg-emerald-50 text-emerald-700 border-emerald-200",
            failed: "bg-red-50 text-red-700 border-red-200",
            queued: "bg-gray-100 text-gray-500 border-gray-200",
        };
        return <span className={`text-xs px-2 py-0.5 rounded font-bold border ${map[s] || ""}`}>{s}</span>; // map['sent'] = ..
    }

    return (
        <>
            <Navbar />
            <div className='min-h-screen bg-gray-50 py-10 px-6'>
                <div className='max-w-5xl mx-auto space-y-8'>
                    <div>
                        <p className='text-xs font-bold uppercase tracking-widest text-indigo-600 mb-1'>
                            Module 6 . AI Emails
                        </p>
                        <h1 className="text-3xl font-extrabold text-gray-900">Email Delivery</h1>
                    </div>

                    
                    {/* KPI cards */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <Kpi label="Delivery Rate" value={`${delivery_rate}%`} color="indigo" />
                        <Kpi label="Total" value={total} color="gray" />
                        <Kpi label="Sent" value={sent} color="emerald" />
                        <Kpi label="Failed" value={failed} color="red" />
                    </div>

                    {/* Delivery Rate bar */}
                    <div className='bg-white border border-gray-200 rounded-2xl p-6 shadow-sm'>
                        <h2 className="text-sm font-bold uppercase tracking-wider text-gray-500 mb-4">Delivery Rate (Metric 4)</h2>
                        <div className="flex items-center gap-4">
                            <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                                <div className="bg-emerald-500 h-4 rounded-full transition-all duration-700"
                                     style={{ width: `${delivery_rate}%` }} />
                            </div>
                            <span className="text-xl font-extrabold text-emerald-700 w-16 text-right shrink-0">{delivery_rate}%</span>
                        </div>
                        <p className="text-xs text-gray-400 mt-3">{sent} sent · {failed} failed · {queued} queued</p>
                    </div>

                        {/* Log table */}
                        <div className='bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden'>
                            <div className='px-6 py-4 border-b border-gray-100'>
                                <h2 className='text-sm font-bold uppercase tracking-wider text-gray-500'>
                                    Recent Emails
                                </h2>
                                <div className='overflow-x-auto'>
                                    <table className="w-full text-sm">
                                        <thead className="bg-gray-50 text-xs font-bold text-gray-500 uppercase tracking-wider">
                                            <tr>
                                                <th className="px-6 py-3 text-left">Type</th>
                                                <th className="px-6 py-3 text-left">Recipient</th>
                                                <th className="px-6 py-3 text-left">Subject</th>
                                                <th className="px-6 py-3 text-left">Status</th>
                                                <th className="px-6 py-3 text-left">Sent At</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-100">
                                            {logs.map((log) => (
                                                <tr key={log.id} className="hover:bg-gray-50">
                                                    <td className="px-6 py-3">
                                                        <span className="text-xs font-semibold text-indigo-600">{log.email_type}</span>
                                                    </td>
                                                    <td className="px-6 py-3 text-gray-700">{log.recipient}</td>
                                                    <td className="px-6 py-3 text-gray-600 max-w-xs truncate">{log.subject}</td>
                                                    <td className="px-6 py-3">{badge(log.status)}</td>
                                                    <td className="px-6 py-3 text-gray-400 text-xs">
                                                        {log.sent_at ? new Date(log.sent_at).toLocaleString() : "—"}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    {/* </div> */}
                </div>
            </div>
        </>
    )
}


function Kpi({ label, value, color }) {
    const colors = {
        indigo: "text-indigo-700 bg-indigo-50 border-indigo-200",
        emerald: "text-emerald-700 bg-emerald-50 border-emerald-200",
        red: "text-red-700 bg-red-50 border-red-200",
        gray: "text-gray-700 bg-gray-50 border-gray-200",
    };
    return (
        <div className={`rounded-2xl border p-5 shadow-sm ${colors[color]}`}>
            <p className="text-xs font-bold uppercase tracking-wider opacity-70 mb-1">{label}</p>
            <p className="text-3xl font-extrabold">{value}</p>
        </div>
    );
}


export default EmailDelivery;