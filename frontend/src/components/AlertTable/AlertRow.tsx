import React from "react";
import { Badge } from "react-bootstrap";
import { AlertItem } from "../../types";
import { formatDate, getLevelVariant } from "../../utils/formatters";

interface AlertRowProps {
    item: AlertItem;
}

export const AlertRow: React.FC<AlertRowProps> = ({ item }) => (
    <tr>
        <td>{item.id}</td>
        <td className="small">{item.file_id}</td>
        <td>
            <Badge bg={getLevelVariant(item.level)}>{item.level}</Badge>
        </td>
        <td>{item.message}</td>
        <td>{formatDate(item.created_at)}</td>
    </tr>
);
