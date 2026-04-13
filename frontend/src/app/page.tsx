"use client";
import React, { useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { DashboardHeader } from "../components/DashboardHeader/DashboardHeader";
import { FileTable } from "../components/FileTable/FileTable";
import { AlertTable } from "../components/AlertTable/AlertTable";
import { UploadModal } from "../components/UploadModal/UploadModal";
import { useDashboard } from "../hooks/useDashboard";

export default function Page() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentAction, setCurrentAction] = useState<string>("");

    const {
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
    } = useDashboard();

    const handleAddFile = (action: string) => {
        setCurrentAction(action);
        setIsModalOpen(true);
    };

    return (
        <Container fluid className="py-4 px-4 bg-light min-vh-100">
            <Row className="justify-content-center">
                <Col xxl={10} xl={11}>
                    <DashboardHeader
                        onRefresh={loadData}
                        onAddFile={handleAddFile}
                    />

                    {errorMessage && (
                        <Alert variant="danger" className="mt-3">
                            {errorMessage}
                        </Alert>
                    )}

                    <FileTable
                        data={filesData}
                        isLoading={isLoading}
                        onDownload={downloadFile}
                        onDelete={deleteFile}
                        onUpdate={updateFile}
                        onPageChange={setFilesPage}
                    />

                    <AlertTable
                        data={alertsData}
                        isLoading={isLoading}
                        onPageChange={setAlertsPage}
                    />
                </Col>
            </Row>

            <UploadModal
                show={isModalOpen}
                onHide={() => setIsModalOpen(false)}
                onSubmit={uploadFile}
                action={currentAction}
            />
        </Container>
    );
}
