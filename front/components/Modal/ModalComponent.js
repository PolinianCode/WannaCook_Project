
import React, { useRef, useEffect } from 'react';
import styles from "../../styles/Modal/Modal.module.css";

export default function Modal({ isOpen, onClose, children}) {
  const modalOverlayRef = useRef();

  const handleModalOverlayClick = (event) => {
    if (modalOverlayRef.current === event.target) {
      onClose();
    }
  };

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (modalOverlayRef.current && !modalOverlayRef.current.contains(event.target)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleOutsideClick);
    }

    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [isOpen, onClose]);

  return (
    <>
      {isOpen && (
        <div className={styles.modalOverlay} ref={modalOverlayRef} onClick={handleModalOverlayClick}>
          <div className={styles.modal}>
            <button className={styles.closeBtn} onClick={onClose}>
              &times;
            </button>
            {children}
          </div>
        </div>
      )}
    </>
  );
}
