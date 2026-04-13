import React from "react";
import { Pagination } from "react-bootstrap";

interface AppPaginationProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
}

export const AppPagination: React.FC<AppPaginationProps> = ({ currentPage, totalPages, onPageChange }) => {
    if (totalPages <= 1) return null;

    return (
        <div className="d-flex justify-content-center mt-4">
            <Pagination className="mb-0">
                <Pagination.First disabled={currentPage === 1} onClick={() => onPageChange(1)} />
                <Pagination.Prev disabled={currentPage === 1} onClick={() => onPageChange(currentPage - 1)} />

                {[...Array(totalPages)].map((_, idx) => (
                    <Pagination.Item
                        key={idx + 1}
                        active={idx + 1 === currentPage}
                        onClick={() => onPageChange(idx + 1)}
                    >
                        {idx + 1}
                    </Pagination.Item>
                ))}

                <Pagination.Next disabled={currentPage === totalPages} onClick={() => onPageChange(currentPage + 1)} />
                <Pagination.Last disabled={currentPage === totalPages} onClick={() => onPageChange(totalPages)} />
            </Pagination>
        </div>
    );
};
