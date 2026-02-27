'use client';

import './globals.css';

export default function RootLayout({ children }) {
  return (
    <html lang="vi">
      <head>
        <title>Deep Research — AI Startup Planner</title>
        <meta name="description" content="AI tạo sản phẩm. Con người vận hành dịch vụ." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        {children}
      </body>
    </html>
  );
}
