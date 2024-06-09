// // src/PdfViewer.jsx

// import React, { useState } from 'react';
// import { Document, Page, pdfjs } from 'react-pdf';
// import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
// import 'react-pdf/dist/esm/Page/TextLayer.css';

// pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

// const PdfViewer = ({ file }) => {
//   const [numPages, setNumPages] = useState(null);
//   const [pageNumber, setPageNumber] = useState(1);

//   function onDocumentLoadSuccess({ numPages }) {
//     setNumPages(numPages);
//     setPageNumber(1);
//   }

//   function changePage(offset) {
//     setPageNumber(prevPageNumber => prevPageNumber + offset);
//   }

//   function previousPage() {
//     changePage(-1);
//   }

//   function nextPage() {
//     changePage(1);
//   }

//   return (
//     <div className="pdf-viewer">
//       <Document file={file} onLoadSuccess={onDocumentLoadSuccess}>
//         <Page pageNumber={pageNumber} />
//       </Document>
//       <div>
//         <div className="page-controls">
//           Page {pageNumber || (numPages ? 1 : '--')} of {numPages || '--'}
//         </div>
//         <div className="button-controls">
//           <button type="button" disabled={pageNumber <= 1} onClick={previousPage}>
//             Previous
//           </button>
//           <button type="button" disabled={pageNumber >= numPages} onClick={nextPage}>
//             Next
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default PdfViewer;
