"use client"

import { useState } from "react";
import Header from "@/app/components/HeaderComponent"
import Modal from "@/app/components/dialogsComponents/ModalComponent";
import AuthModal from "../components/dialogsComponents/AuthModalComponent";



export default function Home() {

  const [isModalOpen, setModalOpen] = useState(false);

  const handleOpenModal = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };
 
  return (
    <div>
      <Header onOpenModal={handleOpenModal} />

      <Modal isOpen={isModalOpen} onClose={handleCloseModal}>
        <AuthModal />
      </Modal>
    </div>
  )
}
