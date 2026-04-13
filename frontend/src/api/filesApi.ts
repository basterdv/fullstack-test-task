import {FileItem, AlertItem, PaginatedResponse} from "../types";

const BASE_URL_DATA = process.env.NEXT_PUBLIC_API_DATA_URL || "http://localhost:8001";
const BASE_URL_UPLOAD = process.env.NEXT_PUBLIC_API_UPLOAD_URL || "http://localhost:8001";

const checkStatus = async (res: Response) => {
    if (!res.ok) throw res;
    if (res.status === 204) return Promise.resolve({} as any);
    return res.json();
};

export const DashboardAPI = {
    fetchFiles: (page: number = 1, size: number = 5): Promise<PaginatedResponse<FileItem>> =>
        fetch(`${BASE_URL_DATA}/files?page=${page}&size=${size}`).then(checkStatus),


    fetchAlerts: (page: number = 1, size: number = 5): Promise<PaginatedResponse<AlertItem>> =>
        fetch(`${BASE_URL_DATA}/alerts?page=${page}&size=${size}`).then(checkStatus),

    getFileDownloadUrl: (fileId: string, action: string) => {
        return `${BASE_URL_DATA}/files/${fileId}/download?action=${action}`;
    },

    uploadFile: (title: string, action: string, file: File): Promise<FileItem> => {
        const formData = new FormData();
        formData.append("title", title);
        formData.append("action", action);
        formData.append("file", file);

        return fetch(`${BASE_URL_UPLOAD}/files`, {
            method: "POST",
            body: formData,
        }).then(checkStatus);
    },

    updateFile: (fileId: string, title: string, action: string): Promise<FileItem> => {
        return fetch(`${BASE_URL_DATA}/files/${fileId}`, {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title, action}),
        }).then(checkStatus);
    },

    deleteFile: (fileId: string, action: string): Promise<void> => {
        return fetch(`${BASE_URL_DATA}/files/${fileId}`, {
            method: "DELETE",
        }).then(checkStatus);
    }
};
