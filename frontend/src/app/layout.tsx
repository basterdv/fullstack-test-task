import type {Metadata} from "next";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container} from "react-bootstrap";

export const metadata: Metadata = {
    title: 'Тестовое задание Fullstack',
    description: 'Система управления файлами',
};

export default function RootLayout({children}: Readonly<{ children: React.ReactNode; }>) {
    return (
        <html lang='ru'>
        <head>
            <link rel="icon" href="/favicon.ico"/>
        </head>
        <body>
        <main>
            <Container fluid className='p-0 min-vh-100'>
                {children}
            </Container>
        </main>
        </body>
        </html>
    );
}
