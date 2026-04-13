import { Badge, Button, ButtonGroup } from "react-bootstrap";
import { FileItem, FileAction } from "../../types";
import { formatSize, formatDate, getProcessingVariant } from "../../utils/formatters";

export interface FileRowProps {
    file: FileItem;
    onDownload: (id: string, action: FileAction) => void;
    onDelete: (id: string, action: FileAction) => void;
    onUpdate: (file: FileItem, action: FileAction) => void;
}

export const FileRow = ({ file, onDownload, onDelete, onUpdate }: FileRowProps) => (
    <tr>
        <td>
            <div className="fw-semibold">{file.title}</div>
            <div className="small text-secondary">{file.id}</div>
        </td>
        <td>{file.original_name}</td>
        <td>{file.mime_type}</td>
        <td>{formatSize(file.size)}</td>
        <td>
            <Badge bg={getProcessingVariant(file.processing_status)}>
                {file.processing_status}
            </Badge>
        </td>
        <td>
            <div className="d-flex flex-column gap-1">
                <Badge bg={file.requires_attention ? "warning" : "success"}>
                    {file.scan_status ?? "pending"}
                </Badge>
                <span className="small text-secondary">
                    {file.scan_details ?? "Ожидает обработки"}
                </span>
            </div>
        </td>
        <td>{formatDate(file.created_at)}</td>
        <td className="text-center">
            <ButtonGroup size="sm">
                <Button variant="outline-warning" onClick={() => onUpdate(file, 'update')}>Изменить</Button>
                <Button variant="outline-primary" onClick={() => onDownload(file.id, 'download')}>Скачать</Button>
                <Button variant="outline-danger" onClick={() => onDelete(file.id, 'delete')}>Удалить</Button>
            </ButtonGroup>
        </td>
    </tr>
);
