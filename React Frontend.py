import React, { useState, useEffect } from "react";
import axios from "axios";
import { Button, Input, Card, CardContent } from "@/components/ui";

const TestCases = () => {
  const [testCases, setTestCases] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [selectedTestCase, setSelectedTestCase] = useState(null);
  const [testSteps, setTestSteps] = useState([]);
  const [action, setAction] = useState("");
  const [selectorType, setSelectorType] = useState("");
  const [selectorValue, setSelectorValue] = useState("");
  const [inputData, setInputData] = useState("");
  const [executionLogs, setExecutionLogs] = useState("");
  const [reportUrl, setReportUrl] = useState(null);

  useEffect(() => {
    fetchTestCases();
  }, []);

  const fetchTestCases = async () => {
    try {
      const response = await axios.get("http://localhost:5000/test_cases");
      setTestCases(response.data);
    } catch (error) {
      console.error("Error fetching test cases", error);
    }
  };

  const createTestCase = async () => {
    try {
      await axios.post("http://localhost:5000/test_cases", { name, description });
      setName("");
      setDescription("");
      fetchTestCases();
    } catch (error) {
      console.error("Error creating test case", error);
    }
  };

  const executeTestCase = async () => {
    try {
      const response = await axios.post(`http://localhost:5000/execute_test/${selectedTestCase}`);
      setExecutionLogs(response.data.logs);
      setReportUrl(response.data.report_url);
    } catch (error) {
      console.error("Error executing test case", error);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Test Cases</h1>
      <div className="flex gap-2 my-4">
        <Input
          type="text"
          placeholder="Test Case Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <Button onClick={createTestCase}>Add</Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {testCases.map((testCase) => (
          <Card key={testCase.id} className="p-2" onClick={() => setSelectedTestCase(testCase.id)}>
            <CardContent>
              <h2 className="text-lg font-semibold">{testCase.name}</h2>
              <p>{testCase.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>
      {selectedTestCase && (
        <div className="mt-4">
          <h2 className="text-lg font-bold">Execute Test Case</h2>
          <Button onClick={executeTestCase} className="my-2">Run Test</Button>
          {executionLogs && (
            <div className="bg-gray-100 p-2 mt-2">
              <h3 className="text-md font-semibold">Execution Logs:</h3>
              <pre className="text-sm">{executionLogs}</pre>
            </div>
          )}
          {reportUrl && (
            <div className="mt-2">
              <a href={reportUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
                Download Test Report
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TestCases;
