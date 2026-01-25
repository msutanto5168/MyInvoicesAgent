'use client';

import { useState, useRef, useEffect } from "react";
import Image from "next/image";

export default function Home() {

  // Default dates
  const today = new Date().toISOString().split('T')[0]; // yyyy-mm-dd

 // Function to get 1st of next month
  const getFirstOfNextMonth = (fromDate: string) => {
    const dateObj = new Date(fromDate);
    dateObj.setMonth(dateObj.getMonth() + 1);
    dateObj.setDate(1);
    return dateObj.toISOString().split('T')[0];
  };

  // Function to get invoice number based on due date
  const getInvoiceNumberFromDueDate = (dueDateValue: string) => {
    const baseInvoice = 220; // 00220
    const baseYear = 2026;
    const baseMonth = 1; // February (0 = Jan, 1 = Feb)

    const due = new Date(dueDateValue);
    const monthDiff =
      (due.getFullYear() - baseYear) * 12 +
      (due.getMonth() - baseMonth);

    const invoiceNum = baseInvoice + monthDiff;
    return invoiceNum.toString().padStart(5, "0");
  };

  const [date, setDate] = useState(today);
  const [dueDate, setDueDate] = useState(getFirstOfNextMonth(today));
  const [invoiceNumber, setInvoiceNumber] = useState(getInvoiceNumberFromDueDate(getFirstOfNextMonth(today)));
  const [gst, setGst] = useState("486.25");
  const [loading, setLoading] = useState(false);
  const [emailto, setEmailTo] = useState("michael.sutanto@gmail.com");
  const [emailsubject, setEmailSubject] = useState("");
  const [emailbody, setEmailBody] = useState("");

  const emailBodyRef = useRef<HTMLTextAreaElement | null>(null);

  interface Row {
    description: string;
    amount: number;
  }

  // Table rows state (default 3 rows)
  const [rows, setRows] = useState<Row[]>([
    { description: getDescription(getFirstOfNextMonth(today)), amount: 4862.45 },
    { description: "", amount: 0 },
    { description: "", amount: 0 },
  ]);

  function getDescription(dueDateValue: string) {
    if (!dueDateValue) return "Rent for shop 7/477 Burwood Highway XX 01 - XX DD 2026";

      const due = new Date(dueDateValue);
      const monthName = due.toLocaleString('default', { month: 'long' }); 
      const year = due.getFullYear();
      const month = due.getMonth(); // 0-indexed

      // Get last day of the month
      const lastDay = new Date(year, month + 1, 0).getDate(); // 0th day of next month = last day of current month

      return `Rent for shop 7/477 Burwood Highway ${monthName} 01 - ${monthName} ${lastDay} ${year}`;
  }

  // Function to generate email subject based on due date
  const getEmailSubject = (dueDateValue: string) => {
    if (!dueDateValue) return "Invoice for Vermont South";
    
    const due = new Date(dueDateValue);
    const monthName = due.toLocaleString('default', { month: 'long' });
    const year = due.getFullYear();
    
    return `Invoice for ${monthName} ${year} - Vermont South`;
  };

  const getNonZeroRows = (rows: Row[]): Row[] => {
    return rows.filter((r: Row) => r.amount !== 0);
  };

  const getSubtotal = (rows: Row[]): number => {
    return getNonZeroRows(rows).reduce(
      (sum: number, r: Row) => sum + r.amount,
      0
    );
  };

  // Function to generate email body based on due date and rows
  const getEmailBody = (
    dueDateValue: string,
    rowsData: Row[],
    gstAmount: string
  ) => {
    if (!dueDateValue) return "";

    const due = new Date(dueDateValue);
    const monthName = due.toLocaleString("default", { month: "long" });
    const year = due.getFullYear();
    const day = due.getDate();

    const getDaySuffix = (d: number) => {
      if (d >= 11 && d <= 13) return "th";
      return ["th", "st", "nd", "rd"][Math.min(d % 10, 4)] || "th";
    };

    const dayWithSuffix = `${day}${getDaySuffix(day)}`;

    const subtotal = getSubtotal(rowsData);
    const gstValue = parseFloat(gstAmount) || 0;
    const total = subtotal + gstValue;

    const breakdownLines = getNonZeroRows(rowsData)
      .map(r => `* ${r.description} = $${r.amount.toFixed(2)}`)
      .join("\n");

    return `Hi Hardik,

  Please find attached the rent invoice for ${monthName} ${year}.
  Please pay by the ${dayWithSuffix} of ${monthName}.

  * Total amount payable = $${total.toFixed(2)}

  Breakdown:  
  * GST = $${gstValue.toFixed(2)}
  ${breakdownLines}

  Please pay to the following account:

      Michael Sutanto
      BSB: 083-028
      ACC: 17-800-9379

  Thanks,
  Michael`;
  };

  // Auto-adjust email body textarea height
  useEffect(() => {
    if (emailBodyRef.current) {
      const ta = emailBodyRef.current;
      ta.style.height = "auto";
      ta.style.height = ta.scrollHeight + "px";
    }
  }, [emailbody]);

  // Initialize email subject and body on mount
  useEffect(() => {
    setEmailSubject(getEmailSubject(dueDate));
    setEmailBody(getEmailBody(dueDate, rows, gst));
  }, [dueDate, rows, gst]);

  const handleDateChange = (newDate: string) => {
    setDate(newDate);

    const newDueDate = getFirstOfNextMonth(newDate);
    setDueDate(newDueDate);
    setInvoiceNumber(getInvoiceNumberFromDueDate(newDueDate));

    // Update first row description automatically
    handleRowChange(0, "description", getDescription(newDueDate));
    
    // Update email subject and body
    setEmailSubject(getEmailSubject(newDueDate));
    setEmailBody(getEmailBody(newDueDate, rows, gst));
  };

  const handleDueDateChange = (newDueDate: string) => {
    setDueDate(newDueDate);
    setInvoiceNumber(getInvoiceNumberFromDueDate(newDueDate));
    handleRowChange(0, "description", getDescription(newDueDate));
    
    // Update email subject and body
    setEmailSubject(getEmailSubject(newDueDate));
    setEmailBody(getEmailBody(newDueDate, rows, gst));
  };

  const handleAddRow = () => {
    setRows([...rows, { description: "", amount: 0 }]);
  };

  const handleRemoveRow = (index: number) => {
    setRows(rows.filter((_, i) => i !== index));
  };
  

  const handleRowChange = (index : number, field : keyof Row, value : string) => {
    const newRows = [...rows];
    if (field === "amount") {
      newRows[index][field] = parseFloat(value) as any;
    } else {
      newRows[index][field] = value as any;
    }
    setRows(newRows);
    
    // Update email body when amounts change
    if (field === "amount" && index === 0) {
      setEmailBody(getEmailBody(dueDate, newRows, gst));
    }
  };

  const handleGstChange = (newGst: string) => {
    setGst(newGst);
    // Update email body when GST changes
    setEmailBody(getEmailBody(dueDate, rows, newGst));
  };

  // Auto-adjust textarea heights after render
  useEffect(() => {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach((textarea: HTMLTextAreaElement) => {
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
    });
  }, [rows]); // Only re-run when rows change, not emailbody

  // Function to convert date format from yyyy-mm-dd to "Month Day, Year"
  const formatDateForAPI = (dateStr: string) => {
    const dateObj = new Date(dateStr);
    return dateObj.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  // Function to extract filename from Content-Disposition header
  const extractFilename = (contentDisposition: string | null): string => {
    if (!contentDisposition) return `invoice_${invoiceNumber}.pdf`;
    
    const filenameMatch = contentDisposition.match(/filename=([^;]+)/);
    if (filenameMatch && filenameMatch[1]) {
      return filenameMatch[1].trim();
    }
    
    return `invoice_${invoiceNumber}.pdf`;
  };

  const handleGenerateInvoice = async () => {
    const API_URL = "https://api.invoiceagent.com.au/subway-invoice";
    const API_KEY = "kxLuYXzZ5Q747edWznjq1aROT9lhFua85uoJL1bB";

    setLoading(true);

    const body = {
      date: formatDateForAPI(date),
      due_date: formatDateForAPI(dueDate),
      invoice_number: invoiceNumber,
      items: rows.map(r => ({ description: r.description, amount: r.amount })),
      gst_amount: parseFloat(gst),
      property_line1: "Shop 7/477 Burwood",
      property_line2: "Highway Vermont South"
    };

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Api-Key": API_KEY
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      // Get the base64-encoded response text
      const base64Data = await res.text();
      
      // Check if response is empty
      if (!base64Data) {
        throw new Error("API returned an empty response");
      }

      // Decode base64 to binary
      const binaryString = atob(base64Data);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      
      // Create blob from binary data
      const blob = new Blob([bytes], { type: 'application/pdf' });

      // Extract filename from Content-Disposition header
      const contentDisposition = res.headers.get('Content-Disposition');
      const filename = extractFilename(contentDisposition);

      // Create a download link
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      // Clean up the object URL
      window.URL.revokeObjectURL(link.href);

      console.log(`✅ Invoice downloaded: ${filename}`);

    } catch (err) {
      console.error("Error details:", err);
      const errorMessage = err instanceof Error ? err.message : "Unknown error occurred";
      alert(`Error calling API: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSendEmail = async () => {
    const INVOICE_API_URL = "https://api.invoiceagent.com.au/subway-invoice";
    const EMAIL_API_URL = "https://api.invoiceagent.com.au/send-email";
    const API_KEY = "kxLuYXzZ5Q747edWznjq1aROT9lhFua85uoJL1bB";

    setLoading(true);

    try {
      // Step 1: Generate the PDF invoice
      const invoiceBody = {
        date: formatDateForAPI(date),
        due_date: formatDateForAPI(dueDate),
        invoice_number: invoiceNumber,
        items: rows.map(r => ({ description: r.description, amount: r.amount })),
        gst_amount: parseFloat(gst),
        property_line1: "Shop 7/477 Burwood",
        property_line2: "Highway Vermont South"
      };

      const invoiceRes = await fetch(INVOICE_API_URL, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Api-Key": API_KEY
        },
        body: JSON.stringify(invoiceBody),
      });

      if (!invoiceRes.ok) throw new Error(`Invoice API error! status: ${invoiceRes.status}`);

      // Get the base64-encoded PDF
      const base64PdfData = await invoiceRes.text();
      
      if (!base64PdfData) {
        throw new Error("Invoice API returned an empty response");
      }

      // Extract filename from Content-Disposition header
      const contentDisposition = invoiceRes.headers.get('Content-Disposition');
      const filename = extractFilename(contentDisposition);

      // Step 2: Send the email with the PDF attachment
      const emailAPIBody = {
        to: emailto,
        subject: emailsubject,
        email_body: emailbody,
        pdf_data: base64PdfData,
        pdf_filename: filename
      };

      const emailRes = await fetch(EMAIL_API_URL, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Api-Key": API_KEY
        },
        body: JSON.stringify(emailAPIBody),
      });

      if (!emailRes.ok) {
        const errorText = await emailRes.text();
        throw new Error(`Email API error! status: ${emailRes.status}, message: ${errorText}`);
      }

      const emailResult = await emailRes.json();
      console.log("✅ Email sent successfully:", emailResult);
      
      alert(`Email sent successfully to ${emailto}!`);

    } catch (err) {
      console.error("Error details:", err);
      const errorMessage = err instanceof Error ? err.message : "Unknown error occurred";
      alert(`Error sending email: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    backgroundColor: "#f0f0f0",
    border: "1px solid #ccc",
    borderRadius: "4px",
    padding: "0.6rem",
    boxSizing: "border-box" as const,
    fontSize: "16px" // Prevents zoom on iOS
  };

  const formInputStyle = {
    ...inputStyle,
    width: "100%",     
    maxWidth: "400px"
  };

  const tableInputStyle = {
    ...inputStyle,
    width: "100%"
  };

  const tableNumberInputStyle = {
    ...inputStyle,
    width: "100%"
  };

  return (
    <main style={{ 
      padding: "1rem 1rem", 
      fontFamily: "sans-serif", 
      maxWidth: "800px",
      margin: "0 auto",
      boxSizing: "border-box"
    }}>
      {/* Logo */}
      <div style={{ textAlign: "center", marginBottom: "1.5rem" }}>
        <Image 
          src="/subway-logo.png" 
          alt="Company Logo" 
          width={150} 
          height={60}
          priority
        />
      </div>

      <h1 style={{ fontSize: "1.5rem", marginBottom: "1.5rem" }}>
        <b>Subway Invoice Generator</b>
      </h1>

      <div style={{ marginBottom: "1rem" }}>
        <label style={{ display: "block", marginBottom: "0.3rem", fontWeight: "500" }}>
          Date:
        </label>
        <input
          type="date"
          value={date}
          onChange={e => handleDateChange(e.target.value)}
          style={formInputStyle}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label style={{ display: "block", marginBottom: "0.3rem", fontWeight: "500" }}>
          Due Date:
        </label>
        <input
          type="date"
          value={dueDate}
          onChange={e => handleDueDateChange(e.target.value)}
          style={formInputStyle}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label style={{ display: "block", marginBottom: "0.3rem", fontWeight: "500" }}>
          Invoice Number:
        </label>
        <input
          type="text"
          value={invoiceNumber}
          onChange={e => setInvoiceNumber(e.target.value)}
          placeholder="Invoice Number"
          style={formInputStyle}
        />
      </div>

      <div style={{ marginBottom: "1.5rem", overflowX: "auto" }}>
        <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
          Items:
        </label>
        <table
          style={{
            width: "100%",
            maxWidth: "400px",
            borderCollapse: "collapse",
            marginBottom: "1rem",
          }}
        >
          <thead>
            <tr>
              <th style={{ 
                border: "1px solid #ccc", 
                padding: "0.5rem",
                backgroundColor: "#f9f9f9",
                textAlign: "left"
              }}>
                Description
              </th>
              <th style={{ 
                border: "1px solid #ccc", 
                padding: "0.5rem",
                backgroundColor: "#f9f9f9",
                textAlign: "left",
                width: "120px"
              }}>
                Amount
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={idx}>
                <td style={{ border: "1px solid #ccc", padding: "0.5rem" }}>
                   <textarea                      
                      value={row.description} 
                      onChange={e => handleRowChange(idx, "description", e.target.value)}                     
                      style={{
                        ...tableInputStyle,
                        minHeight: "2.5rem",
                        overflow: "hidden",
                        resize: "none"
                      }}
                      rows={1}
                      onInput={e => {
                        const ta = e.currentTarget;
                        ta.style.height = "auto";
                        ta.style.height = ta.scrollHeight + "px";
                      }}
                    />
                </td>
                <td style={{ border: "1px solid #ccc", padding: "0.5rem", verticalAlign: "top" }}>
                  <input
                    type="number"
                    step="0.01"
                    inputMode="decimal"
                    value={row.amount}
                    onChange={e => handleRowChange(idx, "amount", e.target.value)}
                    style={tableNumberInputStyle}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <button
          onClick={handleAddRow}
          style={{
            padding: "0.5rem 1rem",
            fontSize: "0.9rem",
            borderRadius: "4px",
            marginBottom: "1rem",
            border: "1px solid #ccc",
            backgroundColor: "#fff",
            cursor: "pointer"
          }}
        >
          + Add Row
        </button>
        <button          
          onClick={() => handleRemoveRow(rows.length - 1)}
          style={{
            padding: "0.5rem 1rem",
            marginLeft: "0.5rem",
            fontSize: "0.9rem",
            borderRadius: "4px",
            marginBottom: "1rem",
            border: "1px solid #ccc",
            backgroundColor: "#fff",
            cursor: "pointer"
          }}
        >
          - Remove Row
        </button>
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label style={{ display: "block", marginBottom: "0.3rem", fontWeight: "500" }}>
          GST Amount:
        </label>
        <input
          type="number"
          value={gst}
          onChange={e => handleGstChange(e.target.value)}
          style={formInputStyle}
        />
      </div>

      <button
        onClick={handleGenerateInvoice}
        disabled={loading}
        style={{
          padding: "0.75rem 1.5rem",
          fontSize: "1rem",
          backgroundColor: "#0070f3",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.7 : 1,
          width: "100%",
          maxWidth: "400px"
        }}
      >
        {loading ? "Generating..." : "Generate PDF"}
      </button>
      
      <div style={{ marginBottom: "1rem", marginTop: "50px" }}>
        <label style={{ display: "block", marginBottom: "0.3rem", fontWeight: "500" }}>
          Email To:
        </label>
        <input
          type="text"
          value={emailto}
          onChange={e => setEmailTo(e.target.value)}
          style={formInputStyle}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label style={{ display: "block", marginBottom: "0.3rem", fontWeight: "500" }}>
          Email Subject:
        </label>
        <input
          type="text"
          value={emailsubject}
          onChange={e => setEmailSubject(e.target.value)}
          style={formInputStyle}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label style={{ display: "block", marginBottom: "0.3rem", fontWeight: "500" }}>
          Email Body:
        </label>
        <textarea         
          ref={emailBodyRef}             
          value={emailbody} 
          onChange={e => setEmailBody(e.target.value)}                     
          style={{
            ...formInputStyle,
            minHeight: "2.5rem",
            overflow: "hidden",
            resize: "none"            
          }}
          rows={1}
          onInput={e => {
            const ta = e.currentTarget;
            ta.style.height = "auto";
            ta.style.height = ta.scrollHeight + "px";
          }}
        />
      </div>

      <button
        onClick={handleSendEmail}
        disabled={loading}
        style={{
          padding: "0.75rem 1.5rem",
          fontSize: "1rem",
          backgroundColor: "#00834cff",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.7 : 1,
          width: "100%",
          maxWidth: "400px"
        }}
      >
        {loading ? "Sending..." : "Send Email with Attachment"}
      </button>



    </main>
  );
}