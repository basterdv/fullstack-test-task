import { useState, useEffect, useCallback } from "react";
import { FileItem, AlertItem, PaginatedResponse } from "../types";
import { DashboardAPI } from "../api/filesApi";

export function useDashboard() {
    const [filesData, setFilesData] = useState<PaginatedResponse<FileItem> | null>(null);
    const [alertsData, setAlertsData] = useState<PaginatedResponse<AlertItem> | null>(null);
    const [filesPage, setFilesPage] = useState(1);
    const [alertsPage, setAlertsPage] = useState(1);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const loadFiles = useCallback(async (page: number) => {
        setIsLoading(true);
        try {
            const data = await DashboardAPI.fetchFiles(page);
            setFilesData(data);
        } catch (error) {
            setErrorMessage("Не удалось загрузить файлы");
        } finally {
            setIsLoading(false);
        }
    }, []);
    const loadAlerts = useCallback(async (page: number) => {
        setIsLoading(true);
        try {
            const data = await DashboardAPI.fetchAlerts(page);
            setAlertsData(data);
        } catch (error) {
            setErrorMessage("Не удалось загрузить алерты");
        } finally {
            setIsLoading(false);
        }
    }, []);
    const loadData = useCallback(async () => {
        setErrorMessage(null);
        await Promise.all([loadFiles(filesPage), loadAlerts(alertsPage)]);
    }, [loadFiles, filesPage, loadAlerts, alertsPage]);


    useEffect(() => {
        loadFiles(filesPage);
    }, [filesPage, loadFiles]);

    useEffect(() => {
        loadAlerts(alertsPage);
    }, [alertsPage, loadAlerts]);

    const uploadFile = async (title: string, action: string, file: File) => {
        try {
            await DashboardAPI.uploadFile(title, action, file);
            setFilesPage(1);
            await loadFiles(1);
        } catch (error) {
            throw new Error("Не удалось загрузить файл на сервер");
        }
    };

    const deleteFile = async (fileId: string, action: string) => {
        if (!window.confirm("Вы уверены?")) return;
        try {
            await DashboardAPI.deleteFile(fileId, action);
            await loadFiles(filesPage);
            await loadAlerts(alertsPage);
        } catch (error) {
            setErrorMessage("Не удалось удалить файл");
        }
    };

    const updateFile = async (file: FileItem, action: string) => {
        const newTitle = window.prompt("Введите новое название:", file.title);
        if (newTitle && newTitle !== file.title) {
            try {
                await DashboardAPI.updateFile(file.id, newTitle, action);
                await loadFiles(filesPage);
            } catch (error) {
                setErrorMessage("Не удалось обновить название");
            }
        }
    };

    const downloadFile = useCallback((fileId: string, action: string) => {
        window.location.href = DashboardAPI.getFileDownloadUrl(fileId, action);
        setTimeout(() => loadAlerts(alertsPage), 1000);
    }, [loadAlerts, alertsPage]);

    return {
        filesData,
        alertsData,
        isLoading,
        errorMessage,
        loadData,
        uploadFile,
        downloadFile,
        deleteFile,
        updateFile,
        setFilesPage,
        setAlertsPage,
    };
}
