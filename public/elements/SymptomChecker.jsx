import { Button } from "@/components/ui/button";

export default function SymptomChecker() {
  const symptoms = [
    "Abnormal vaginal bleeding",
    "Pelvic pain",
    "Vaginal discharge",
    "Breast pain/lumps",
    "Menstrual irregularities",
    "Pain during intercourse",
    "Urinary problems"
  ];

  const handleSymptomClick = (symptom) => {
    // Send message with the selected symptom
    sendUserMessage(`I'm experiencing ${symptom}`);
  };

  return (
    <div className="mt-4 flex flex-col gap-3 p-4 border rounded-md bg-slate-50">
      <h3 className="text-lg font-medium mb-2">Common Symptoms</h3>
      <p className="text-sm text-slate-600 mb-2">Click on any symptoms you're experiencing:</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        {symptoms.map((symptom) => (
          <Button
            key={symptom}
            variant="outline"
            className="justify-start text-left"
            onClick={() => handleSymptomClick(symptom)}
          >
            {symptom}
          </Button>
        ))}
      </div>
    </div>
  );
}