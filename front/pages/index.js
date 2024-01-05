import { useRouter } from "next/dist/client/router"
import Header from "../components/Header/HeaderComponent"
import { useState } from "react"
import Modal from "../components/Modal/ModalComponent"
import AuthModal from "../components/Modal/AuthModalComponent"


export default function Home() {

  const [showModal, setShowModal] = useState(false);
  const router = useRouter()

 

  return (
    <>
      <Header onOpenModal={() => setShowModal(true)}/>

      {showModal && (
        <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
          <AuthModal />
        </Modal>
      )}
    </>
  )
}
