'use client';

import { useState, useRef, useEffect } from "react";

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

  const [date, setDate] = useState(today);
  const [dueDate, setDueDate] = useState(getFirstOfNextMonth(today));
  const [invoiceNumber, setInvoiceNumber] = useState("00220");
  const [gst, setGst] = useState("486.25");
  const [loading, setLoading] = useState(false);


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

  const handleDateChange = (newDate: string) => {
    setDate(newDate);

    const newDueDate = getFirstOfNextMonth(newDate);
    setDueDate(newDueDate);

    // Update first row description automatically
    handleRowChange(0, "description", getDescription(newDueDate));
  };

  const handleAddRow = () => {
    setRows([...rows, { description: "", amount: 0 }]);
  };
  

  const handleRowChange = (index : number, field : keyof Row, value : string) => {
    const newRows = [...rows];
    if (field === "amount") {
      newRows[index][field] = parseFloat(value) as any; // TypeScript doesn’t allow number assignment to Row[field] if field is keyof Row
    } else {
      newRows[index][field] = value as any;
    }
    setRows(newRows);
  };

  const handleGenerateInvoice = async () => {
    setLoading(true);

    const body = {
      date,
      due_date: dueDate,
      invoice_number: invoiceNumber,
      items: rows.map(r => ({ description: r.description, amount: r.amount })),
      gst_amount: parseFloat(gst)
    };

    try {
      const res = await fetch("/api/invoice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();

      if (data.isBase64Encoded && data.body) {
        const link = document.createElement("a");
        link.href = `data:application/pdf;base64,${data.body}`;
        link.download = "invoice.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        alert("Error generating invoice");
      }
    } catch (err) {
      console.error(err);
      alert("Error calling API");
    }

    setLoading(false);
  };

  const inputStyle = {
    backgroundColor: "#f0f0f0",
    border: "1px solid #ccc",
    borderRadius: "4px",
    padding: "0.4rem 0.6rem",
    width: "100%",
    boxSizing: "border-box" as const
  };

  const numberInputStyle = {
    ...inputStyle,
    width: "100px"
  };

  return (
    <main style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h1><b>Subway Invoice Generator</b></h1>

      <div style={{ marginBottom: "1rem", marginTop: "10px" }}>
        <label>Date: </label>
        <input
          type="date"
          value={date}
          onChange={e => handleDateChange(e.target.value)}
          style={inputStyle}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>Due Date: </label>
        <input
          style={inputStyle}
          type="date"
          value={dueDate}
          onChange={e => {
            setDueDate(e.target.value);
            // update first row description automatically
            handleRowChange(0, "description", getDescription(e.target.value));
          }}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>Invoice Number: </label>
        <input
          style={inputStyle}
          type="text"
          value={invoiceNumber}
          onChange={e => setInvoiceNumber(e.target.value)}
          placeholder="Invoice Number"
        />
      </div>

      <div style={{ marginBottom: "1rem", overflowX: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginBottom: "1rem",
          }}
        >
          <thead>
            <tr>
              <th style={{ border: "1px solid #ccc", padding: "0.5rem" }}>Description</th>
              <th style={{ border: "1px solid #ccc", padding: "0.5rem" }}>Amount</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={idx}>
                <td style={{ border: "1px solid #ccc", padding: "0.5rem", maxWidth: "300px" }}>
                   <textarea                      
                      value={row.description} 
                      onChange={e => handleRowChange(idx, "description", e.target.value)}                     
                      style={{
                        ...inputStyle,
                        minHeight: "1.5rem",
                        overflow: "hidden",
                        resize: "none"
                      }}
                      rows={1}
                      onInput={e => {
                        const ta = e.currentTarget;
                        ta.style.height = "auto";           // reset height
                        ta.style.height = ta.scrollHeight + "px"; // adjust to content
                      }}
                    />
                </td>
                <td style={{ border: "1px solid #ccc", padding: "0.5rem", verticalAlign: "top" }}>
                  <input
                    type="number"
                    value={row.amount}
                    onChange={e => handleRowChange(idx, "amount", e.target.value)}
                    style={numberInputStyle}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <button
          onClick={handleAddRow}
          style={{
            padding: "0.3rem 0.6rem",
            fontSize: "0.9rem",
            borderRadius: "4px",
            marginBottom: "1rem",
          }}
        >
          + Add Row
        </button>
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>GST Amount: </label>
        <input
          type="number"
          value={gst}
          onChange={e => setGst(e.target.value)}
          style={inputStyle}
        />
      </div>

      <button
        onClick={handleGenerateInvoice}
        disabled={loading}
        style={{
          padding: "0.5rem 1rem",
          fontSize: "1rem",
          backgroundColor: "#0070f3",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
        }}
      >
        {loading ? "Generating..." : "Generate PDF"}
      </button>
    </main>
  );
}
