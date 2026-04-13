import React from "react";
import { Badge, Card, Spinner, Table } from "react-bootstrap";
import { FileTableProps } from "../../types";
import { FileRow } from "./FileRow";
import { AppPagination } from "../Pagination/Pagination";

export const FileTable: React.FC<FileTableProps> = ({
    data,
    isLoading,
    onDownload,
    onDelete,
    onUpdate,
    onPageChange,
}) => {
    const files = data?.items || [];
    const { page = 1, pages = 0, total = 0 } = data || {};

    const renderContent = () => {
        if (isLoading) {
            return (
                <div className="d-flex justify-content-center py-5">
                    <Spinner animation="border" />
                </div>
            );
        }

        return (
            <>
                <div className="table-responsive">
                    <Table hover bordered className="align-middle mb-0">
                        <thead className="table-light">
                            <tr>
                                <th>Название</th>
                                <th>Файл</th>
                                <th>MIME</th>
                                <th>Размер</th>
                                <th>Статус</th>
                                <th>Проверка</th>
                                <th>Создан</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {files.length === 0 ? (
                                <tr>
                                    <td colSpan={8} className="text-center py-4 text-secondary">
                                        Файлы пока не загружены
                                    </td>
                                </tr>
                            ) : (
                                files.map((file) => (
                                    <FileRow
                                        key={file.id}
                                        file={file}
                                        onDownload={onDownload}
                                        onDelete={onDelete}
                                        onUpdate={onUpdate}
                                    />
                                ))
                            )}
                        </tbody>
                    </Table>
                </div>

                <AppPagination
                    currentPage={page}
                    totalPages={pages}
                    onPageChange={onPageChange}
                />
            </>
        );
    };

    return (
        <Card className="shadow-sm border-0 mb-4">
            <Card.Header className="bg-white border-0 pt-4 px-4">
                <div className="d-flex justify-content-between align-items-center">
                    <h2 className="h5 mb-0">Файлы</h2>
                    <Badge bg="secondary">{total}</Badge>
                </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
                {renderContent()}
            </Card.Body>
        </Card>
    );
};
