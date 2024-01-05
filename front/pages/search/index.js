'use client'
import Header from "../../components/Header/HeaderComponent";
import { useRouter } from "next/router";
import Container from "../../components/Basic/ContainerComponent";
import Modal from "../../components/Modal/ModalComponent";

import { useState } from "react";
import AuthModal from "../../components/Modal/AuthModalComponent";

export default function SearchResult() {
    const router = useRouter();
    const { data } = router.query;

    

    const [showModal, setShowModal] = useState(false);

    try {
        const searchData = JSON.parse(decodeURIComponent(data));

        if (!searchData.search_results || searchData.search_results.length === 0) {
            return (
                <>
                    <Header onOpenModal={() => setShowModal(true)} />
                    <Container>
                        <div>Nothing was found</div>
                    </Container>
                </>
            );
        }

        return (
            <>
                <Header onOpenModal={() => setShowModal(true)}/>
                <Container>
                    <div>
                        <ul>
                            {searchData.search_results.map((result) => (
                                <li key={result.recipe_id}>{result.title}</li>
                            ))}
                        </ul>
                    </div>
                </Container>   
                {showModal && (
                    <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
                        <AuthModal />
                    </Modal>
                )}       
            </>
        );
    } catch (error) {
        console.error('JSON error:', error);
    }
}
