
import React, { useState } from 'react';
import { Upload, FileText, Trash2, Loader2 } from 'lucide-react';
import axios from 'axios';

interface SidebarProps {
    onUploadSuccess: (filename: string) => void;
    onClear: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onUploadSuccess, onClear }) => {
    const [uploading, setUploading] = useState(false);
    const [fileList, setFileList] = useState<string[]>(() => {
        const saved = localStorage.getItem('uploadedFiles');
        return saved ? JSON.parse(saved) : [];
    });

    React.useEffect(() => {
        localStorage.setItem('uploadedFiles', JSON.stringify(fileList));
    }, [fileList]);

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        if (file.type !== 'application/pdf') {
            alert('Only PDF files are supported.');
            return;
        }

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setFileList(prev => [...prev, file.name]);
            onUploadSuccess(file.name);
        } catch (error) {
            console.error('Upload failed', error);
            alert('Failed to upload file.');
        } finally {
            setUploading(false);
            // Reset input value to allow re-uploading same file if needed
            event.target.value = '';
        }
    };

    const handleClear = async () => {
        try {
            await axios.delete('http://localhost:8000/clear');
            setFileList([]);
            localStorage.removeItem('uploadedFiles');
            onClear();
        } catch (error) {
            console.error('Clear failed', error);
        }
    };

    return (
        <div className="w-64 bg-white border-r border-gray-200 h-full p-4 flex flex-col shadow-sm">
            <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                <FileText className="text-blue-600" />
                Research AI
            </h2>

            <div className="mb-6">
                <label
                    htmlFor="file-upload"
                    className={`flex items-center justify-center w-full p-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition  ${uploading ? 'opacity-70 cursor-not-allowed' : ''}`}
                >
                    {uploading ? <Loader2 className="animate-spin mr-2" /> : <Upload className="mr-2" size={18} />}
                    {uploading ? 'Uploading...' : 'Upload PDF'}
                </label>
                <input
                    id="file-upload"
                    type="file"
                    accept=".pdf"
                    className="hidden"
                    onChange={handleFileChange}
                    disabled={uploading}
                />
            </div>

            <div className="flex-1 overflow-y-auto">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Documents</h3>
                {fileList.length === 0 ? (
                    <p className="text-sm text-gray-400 italic">No documents uploaded</p>
                ) : (
                    <ul className="space-y-2">
                        {fileList.map((file, idx) => (
                            <li key={idx} className="flex items-center text-sm text-gray-700 p-2 bg-gray-50 rounded">
                                <FileText size={16} className="text-gray-400 mr-2" />
                                <span className="truncate">{file}</span>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            <div className="mt-auto pt-4 border-t border-gray-100">
                <button
                    onClick={handleClear}
                    className="flex items-center justify-center w-full p-2 text-red-600 hover:bg-red-50 rounded-lg transition text-sm"
                >
                    <Trash2 size={16} className="mr-2" />
                    Clear History
                </button>
            </div>
        </div>
    );
};
