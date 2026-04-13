import {useState} from "react";

interface UseUploadFormProps {
    onSubmit: (title: string, action:string, file: File) => Promise<void>;
    onHide: () => void;
    action: string;
}

export function useUploadForm({onSubmit, onHide,action}: UseUploadFormProps) {
    const [title, setTitle] = useState("")
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const reset = () => {
        setTitle("");
        setSelectedFile(null);
        setError(null);
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedFile(e.target.files?.[0] ?? null);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!title.trim() || !action || !selectedFile ) return;

        setIsSubmitting(true);
        setError(null);

        try {
            await onSubmit(title.trim(), action,selectedFile);
            reset();
            onHide();
        } catch (err) {
            setError("Не удалось загрузить файл. Попробуйте еще раз.");
        } finally {
            setIsSubmitting(false);
        }
    };

    return {title, setTitle, isSubmitting, error, handleFileChange, handleSubmit, reset};
}
