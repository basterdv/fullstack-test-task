export type FileItem = {
  id: string;
  title: string;
  original_name: string;
  mime_type: string;
  size: number;
  processing_status: string;
  scan_status: string | null;
  scan_details: string | null;
  requires_attention: boolean;
  created_at: string;
};

export type AlertItem = {
  id: number;
  file_id: string;
  level: string;
  message: string;
  created_at: string;
};

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export type FileAction = 'download' | 'delete' | 'update';

export interface FileTableProps {
  data: PaginatedResponse<FileItem> | null;
  isLoading: boolean;
  onDownload: (fileId: string, action: FileAction) => void;
  onDelete: (fileId: string, action: FileAction) => void;
  onUpdate: (file: FileItem, action: FileAction) => void;
  onPageChange: (page: number) => void;
}

export interface AlertTableProps {
  data: PaginatedResponse<AlertItem> | null;
  isLoading: boolean;
  onPageChange: (page: number) => void;
}