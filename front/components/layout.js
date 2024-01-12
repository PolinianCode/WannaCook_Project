import Container from "./Basic/ContainerComponent";
import Header from "./Header/HeaderComponent";
import AuthModal from "./Modal/AuthModalComponent";
import Modal from "./Modal/ModalComponent";
import { useState } from "react"

export default function Layout({ children }) {

    const [showModal, setShowModal] = useState(false);

    const openModal = () => {
        setShowModal(true);
      };

    return (
        <>
            <Header onOpenModal={openModal}/>
            {showModal && (
                <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
                    <AuthModal />
                </Modal>
            )}

            <Container>
                {children}
            </Container>
        </>
    )
    }