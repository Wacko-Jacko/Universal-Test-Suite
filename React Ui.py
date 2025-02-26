import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";
import { toast } from "react-hot-toast";

export default function TestCases() {
  const [testCases, setTestCases] = useState([]);
  const [testResults, setTestResults] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTestCases();
    fetchTestResults();
  }, []);

  const fetchTestCases = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:5000/test_cases");
      setTestCases(response.data);
    } catch (error) {
      toast.error("Failed to fetch test cases");
    }
    setLoading(false);
  };

  const fetchTestResults = async () => {
    try {
      const response = await axios.get("http://localhost:5000/test_results");
      setTestResults(response.data);
    } catch (error) {
      toast.error("Failed to fetch test results");
    }
  };

  const addTestCase = async () => {
    if (!name || !description) {
      toast.error("Please enter both name and description");
      return;
    }
    setLoading(true);
    try {
      await axios.post("http://localhost:5000/test_cases", { name, description });
      toast.success("Test case added successfully");
      fetchTestCases();
      setName("");
      setDescription("");
    } catch (error) {
      toast.error("Failed to add test case");
    }
    setLoading(false);
  };

  const executeTest = async (id) => {
    setLoading(true);
    try {
      await axios.post(`http://localhost:5000/execute_test/${id}`);
      toast.success("Test execution started!");
      fetchTestResults();
    } catch (error) {
      toast.error("Failed to execute test");
    }
    setLoading(false);
  };

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold text-center">Test Cases</h1>
      <div className="my-6 flex gap-2 items-center">
        <Input placeholder="Test Name" value={name} onChange={(e) => setName(e.target.value)} />
        <Input placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <Button onClick={addTestCase} disabled={loading}>
          {loading ? <Loader2 className="animate-spin" /> : "Add Test"}
        </Button>
      </div>
      {loading && <p className="text-center">Loading...</p>}
      <div className="grid gap-4">
        {testCases.map((test) => (
          <Card key={test.id} className="p-4 border border-gray-200 rounded-lg shadow-md">
            <CardContent>
              <h2 className="text-lg font-semibold">{test.name}</h2>
              <p className="text-gray-600">{test.description}</p>
              <Button className="mt-2" onClick={() => executeTest(test.id)} disabled={loading}>
                {loading ? <Loader2 className="animate-spin" /> : "Run Test"}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
      <h2 className="text-2xl font-bold text-center mt-8">Test Results</h2>
      <div className="grid gap-4 mt-4">
        {testResults.map((result) => (
          <Card key={result.id} className="p-4 border border-gray-200 rounded-lg shadow-md">
            <CardContent>
              <h3 className="text-lg font-semibold">{result.test_name}</h3>
              <p>Status: <span className={result.status === 'Passed' ? "text-green-500" : "text-red-500"}>{result.status}</span></p>
              <p>Executed At: {new Date(result.executed_at).toLocaleString()}</p>
              {result.screenshot && (
                <img src={`http://localhost:5000/${result.screenshot}`} alt="Screenshot" className="mt-2 max-w-xs" />
              )}
              <p className="text-sm text-gray-500">Logs: {result.logs}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
