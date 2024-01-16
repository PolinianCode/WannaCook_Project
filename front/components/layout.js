import Container from "./Basic/ContainerComponent";
import Header from "./Header/HeaderComponent";
import AuthModal from "./Modal/AuthModalComponent";
import Modal from "./Modal/ModalComponent";
import AddRecipeButtonComponent from "./Basic/addRecipeButtomComponent";
import { useState } from "react"
import FooterComponent from "./Footer/FooterComponent";

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
            <AddRecipeButtonComponent />
            {/* <FooterComponent /> */}
        </>
    )
    }