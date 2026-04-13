import React from "react";
import {Button, Form, Modal, Alert} from "react-bootstrap";
import {useUploadForm} from "../../hooks/useUploadForm";

interface UploadModalProps {
    show: boolean;
    onHide: () => void;
    onSubmit: (title: string, action:string, file: File) => Promise<void>;
    action: string;
}

export const UploadModal = ({show, onHide, onSubmit,action}: UploadModalProps) => {
    const {
        title, setTitle, isSubmitting, error,
        handleFileChange, handleSubmit
    } = useUploadForm({onSubmit, onHide,action});

    return (
        <Modal show={show} onHide={onHide} centered>
            <Form onSubmit={handleSubmit}>
                <Modal.Header closeButton>
                    <Modal.Title>Добавить файл</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    {error && <Alert variant="danger">{error}</Alert>}

                    <Form.Group className="mb-3">
                        <Form.Label>Название</Form.Label>
                        <Form.Control
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            placeholder="Например, Договор"
                            required
                        />
                    </Form.Group>

                    <Form.Group>
                        <Form.Label>Файл</Form.Label>
                        <Form.Control
                            type="file"
                            onChange={handleFileChange}
                            required
                        />
                    </Form.Group>
                </Modal.Body>

                <Modal.Footer>
                    <Button variant="outline-secondary" onClick={onHide}>Отмена</Button>
                    <Button type="submit" variant="primary" disabled={isSubmitting}>
                        {isSubmitting ? "Загрузка..." : "Сохранить"}
                    </Button>
                </Modal.Footer>
            </Form>
        </Modal>
    );
};
