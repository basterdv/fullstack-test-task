import React from "react";
import { Badge, Card, Spinner, Table } from "react-bootstrap";
import { AlertTableProps } from "../../types";
import { AlertRow } from "./AlertRow";
import { AppPagination } from "../Pagination/Pagination";

export const AlertTable: React.FC<AlertTableProps> = ({ data, isLoading, onPageChange }) => {
    const alerts = data?.items || [];
    const { page = 1, pages = 0, total = 0 } = data || {};

    const renderBody = () => {
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
                                <th>ID</th>
                                <th>File ID</th>
                                <th>Уровень</th>
                                <th>Сообщение</th>
                                <th>Создан</th>
                            </tr>
                        </thead>
                        <tbody>
                            {alerts.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="text-center py-4 text-secondary">
                                        Алертов пока нет
                                    </td>
                                </tr>
                            ) : (
                                alerts.map((item) => <AlertRow key={item.id} item={item} />)
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
        <Card className="shadow-sm border-0">
            <Card.Header className="bg-white border-0 pt-4 px-4">
                <div className="d-flex justify-content-between align-items-center">
                    <h2 className="h5 mb-0">Алерты</h2>
                    <Badge bg="secondary">{total}</Badge>
                </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
                {renderBody()}
            </Card.Body>
        </Card>
    );
};
