const NotFound = ( {headingTitle, pageText} ) => {
    const containerStyle = {
      textAlign: 'center',
      width: '100%',
      marginTop: '2em',
      display: 'flex',
      justifyContent: 'center',
      flexDirection: 'column',
    };
  
    const headingStyle = {
      fontSize: '2em',
      color: '#333',
    };
  
    const paragraphStyle = {
      fontSize: '1.2em',
      color: '#666',
    };
  
    return (
      <div style={containerStyle}>
        <h2 style={headingStyle}>{headingTitle}</h2>
        <p style={paragraphStyle}>{pageText}</p>
      </div>
    );
  };
  
  export default NotFound;