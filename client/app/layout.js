import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Wanna Cook',
  description: 'Miejscu dla miłośników gotowania! Odkrywaj przepisy, cenne wskazówki i recenzje sprzętu kuchennego. Niezależnie od poziomu doświadczenia, znajdziesz tu inspiracje do tworzenia smacznych potraw na co dzień i od święta. Dołącz do społeczności Wanna Cook i dziel się swoją pasją kulinarą!',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
