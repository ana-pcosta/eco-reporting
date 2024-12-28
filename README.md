# eco-reporting

## Context
From 2025 onwards, over 50.000 companies in the EU need to report about sustainability matters based on the newly created ESRS (European Sustainability Reporting Standards). These strict standards for sustainability reporting are written down in a >200 pages explanation. (https://xbrl.efrag.org/e-esrs/esrs-set1-2023.html)
Our product helps sustainability teams to generate ESRS conform reporting text based on existing document’s information. It also helps to check, whether or not the generated or written reporting text is already fulfilling the strict standards correctly

### Prompt-Engineering Task
One part of the standard is about Climate Change (E1).
When companies report about climate change, they have to disclose their “Transition plan for climate change mitigation” (E1-1). You can find a best practice example of a danish energy company (Ørsted) here:
(Pages 87 to 89, 91) https://orstedcdn.azureedge.net/-/media/annual-report-2023/orsted-ar-2023.pdf?rev=526307f68e2047b3a1df8dd2cdf719ec&hash=E6069E12C1792AD620FA12898587394C
Attached to this e-mail, you can find the detailed explanation of how “Disclosure Requirement E1-1 – Transition plan for climate change mitigation” needs to be reported.
1. Build a prompt(-chain), that analyses if the report of TAKKT (https://www.takkt.de/fileadmin/user_upload/takkt/nachhaltigkeit/NHB23_Corporate_Responsibility_en.pdf) from 2023 is fulfilling the reporting requirements for E1-1 completely, or if there are still "gaps" in the written report. The result should be a list of found gaps. The gaps should provide an exact explanation, of what is still missing in comparison to what the standard actually asks for.
2. Ideation: What other features (related to checking existing report text) could be helpful for a user and are possible to implement with LLMs?
Provide one or multiple prompts that fulfill the requirements and an example output of the prompts when you run it for the TAKKT report.

### Architecture Task
We want to find valuable information within Documents, that we can provide as context, when generating report texts.
1. How would an Architecture look that finds and provides valuable information from existing documents as context, when generating report text?
2. How would you extract various different documents information? (PDFs, Excels, PPTX, Words, …)
3. How would you break document information into pieces?
4. What different options do you see for the classification/search?