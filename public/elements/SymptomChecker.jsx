// public/elements/SymptomChecker.jsx
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";

export default function SymptomChecker() {
  const [step, setStep] = useState(1);
  const [selectedAreas, setSelectedAreas] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [personalInfo, setPersonalInfo] = useState({
    age: "",
    height: "",
    weight: "",
    lastPeriod: "",
  });
  const [additionalInfo, setAdditionalInfo] = useState("");

  // Body areas for step 1
  const bodyAreas = [
    "Vaginal",
    "Pelvic",
    "Uterine",
    "Breast",
    "Urinary",
    "General"
  ];

  // Symptoms by area for step 2
  const symptomsByArea = {
    "Vaginal": ["Discharge", "Bleeding", "Itching", "Dryness", "Odor"],
    "Pelvic": ["Pain", "Pressure", "Cramping", "Fullness"],
    "Uterine": ["Menstrual irregularities", "Heavy periods", "Spotting", "Missed periods"],
    "Breast": ["Pain", "Lumps", "Discharge", "Tenderness", "Changes in appearance"],
    "Urinary": ["Frequent urination", "Pain when urinating", "Urgency", "Incontinence"],
    "General": ["Fatigue", "Fever", "Nausea", "Lower back pain", "Abdominal bloating"]
  };

  // Handle selecting a body area in step 1
  const handleAreaClick = (area) => {
    setSelectedAreas(prev => {
      // If already selected, remove it, otherwise add it
      if (prev.includes(area)) {
        return prev.filter(item => item !== area);
      } else {
        return [...prev, area];
      }
    });
  };

  // Handle selecting a symptom in step 2
  const handleSymptomClick = (area, symptom) => {
    const fullSymptom = `${area} ${symptom}`;
    setSelectedSymptoms(prev => {
      if (prev.includes(fullSymptom)) {
        return prev.filter(item => item !== fullSymptom);
      } else {
        return [...prev, fullSymptom];
      }
    });
  };

  // Handle personal info changes in step 3
  const handlePersonalInfoChange = (field, value) => {
    setPersonalInfo(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Move to next step
  const nextStep = () => {
    setStep(prev => prev + 1);
  };

  // Move to previous step
  const prevStep = () => {
    setStep(prev => prev - 1);
  };

  // Submit final data
  const handleSubmit = () => {
    // Compile all information into a structured message
    const message = `
I'm experiencing the following symptoms:
${selectedSymptoms.join(", ")}

Personal information:
- Age: ${personalInfo.age || "Not provided"}
- Height: ${personalInfo.height || "Not provided"}
- Weight: ${personalInfo.weight || "Not provided"}
- Last period date: ${personalInfo.lastPeriod || "Not provided"}

Additional information:
${additionalInfo || "None provided"}
    `.trim();

    // Send to backend
    sendUserMessage(message);
  };

  // Render based on current step
  const renderStep = () => {
    switch(step) {
      case 1:
        return (
          <Card className="p-4">
            <h3 className="text-md font-medium mb-3">Step 1: Select the body areas where you're experiencing symptoms</h3>
            <div className="flex flex-wrap gap-2 mb-4">
              {bodyAreas.map((area, idx) => (
                <Button
                  key={idx}
                  variant={selectedAreas.includes(area) ? "default" : "outline"}
                  onClick={() => handleAreaClick(area)}
                  className="transition-all hover:shadow-md"
                >
                  {area} Area
                </Button>
              ))}
            </div>

            {selectedAreas.length > 0 && (
              <div className="mt-4 flex justify-end">
                <Button onClick={nextStep} className="flex items-center gap-2">
                  Next
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </Button>
              </div>
            )}
          </Card>
        );

      case 2:
        return (
          <Card className="p-4">
            <h3 className="text-md font-medium mb-3">Step 2: Select specific symptoms you're experiencing</h3>

            {selectedAreas.map((area) => (
              <div key={area} className="mb-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">{area} Area:</h4>
                <div className="flex flex-wrap gap-2">
                  {symptomsByArea[area].map((symptom, idx) => {
                    const fullSymptom = `${area} ${symptom}`;
                    const isSelected = selectedSymptoms.includes(fullSymptom);

                    return (
                      <Button
                        key={idx}
                        variant={isSelected ? "default" : "outline"}
                        onClick={() => handleSymptomClick(area, symptom)}
                        className={`transition-all hover:shadow-md ${isSelected ? "bg-primary text-white" : ""}`}
                      >
                        {symptom}
                      </Button>
                    );
                  })}
                </div>
              </div>
            ))}

            {selectedSymptoms.length > 0 && (
              <div className="mt-4 flex justify-between">
                <Button variant="outline" onClick={prevStep}>
                  Back
                </Button>
                <Button onClick={nextStep} className="flex items-center gap-2">
                  Next
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </Button>
              </div>
            )}
          </Card>
        );

      case 3:
        return (
          <Card className="p-4">
            <h3 className="text-md font-medium mb-3">Step 3: Personal Information</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                <Input
                  type="number"
                  placeholder="Years"
                  value={personalInfo.age}
                  onChange={(e) => handlePersonalInfoChange('age', e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Height</label>
                <Input
                  placeholder="cm or feet/inches"
                  value={personalInfo.height}
                  onChange={(e) => handlePersonalInfoChange('height', e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Weight</label>
                <Input
                  placeholder="kg or lb"
                  value={personalInfo.weight}
                  onChange={(e) => handlePersonalInfoChange('weight', e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Last period date</label>
                <Input
                  placeholder="DD/MM/YYYY"
                  value={personalInfo.lastPeriod}
                  onChange={(e) => handlePersonalInfoChange('lastPeriod', e.target.value)}
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Additional Information</label>
              <textarea
                className="w-full h-24 p-2 border border-gray-300 rounded-md"
                placeholder="Please share any other information that might be relevant..."
                value={additionalInfo}
                onChange={(e) => setAdditionalInfo(e.target.value)}
              ></textarea>
            </div>

            <div className="mt-4 flex justify-between">
              <Button variant="outline" onClick={prevStep}>
                Back
              </Button>
              <Button onClick={nextStep} className="flex items-center gap-2">
                Next
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </Button>
            </div>
          </Card>
        );

      case 4:
        return (
          <Card className="p-4">
            <h3 className="text-md font-medium mb-3">Review Your Information</h3>

            <div className="mb-4">
              <h4 className="text-sm font-medium mb-2">Selected Body Areas:</h4>
              <div className="flex flex-wrap gap-1">
                {selectedAreas.map((area, idx) => (
                  <span key={idx} className="px-2 py-1 bg-gray-100 rounded-full text-sm">
                    {area}
                  </span>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <h4 className="text-sm font-medium mb-2">Symptoms:</h4>
              <div className="flex flex-wrap gap-1">
                {selectedSymptoms.map((symptom, idx) => (
                  <span key={idx} className="px-2 py-1 bg-primary/10 text-primary rounded-full text-sm">
                    {symptom}
                  </span>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <h4 className="text-sm font-medium mb-2">Personal Information:</h4>
              <ul className="list-disc pl-5 text-sm">
                <li>Age: {personalInfo.age || "Not provided"}</li>
                <li>Height: {personalInfo.height || "Not provided"}</li>
                <li>Weight: {personalInfo.weight || "Not provided"}</li>
                <li>Last period: {personalInfo.lastPeriod || "Not provided"}</li>
              </ul>
            </div>

            {additionalInfo && (
              <div className="mb-4">
                <h4 className="text-sm font-medium mb-2">Additional Information:</h4>
                <p className="text-sm bg-gray-50 p-2 rounded">{additionalInfo}</p>
              </div>
            )}

            <div className="mt-4 flex justify-between">
              <Button variant="outline" onClick={prevStep}>
                Back
              </Button>
              <Button onClick={handleSubmit} className="flex items-center gap-2">
                Submit
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </Button>
            </div>
          </Card>
        );

      default:
        return null;
    }
  };

  // Progress bar
  const renderProgressBar = () => {
    const totalSteps = 4;
    return (
      <div className="flex gap-1 mb-4">
        {Array.from({ length: totalSteps }).map((_, index) => (
          <div
            key={index}
            className={`h-1 flex-grow rounded-full ${
              index < step ? "bg-primary" : "bg-gray-200"
            }`}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="flex flex-col gap-3 p-4 bg-gray-50 rounded-md">
      {renderProgressBar()}
      {renderStep()}
    </div>
  );
}