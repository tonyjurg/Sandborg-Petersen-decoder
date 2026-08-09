const { test, expect } = require("@playwright/test");

const decoderPages = [
  { name: "published decoder", path: "/docs/index.html" },
  { name: "standalone decoder", path: "/javascript/SP-Morph-decode.html" },
];

const decodingCases = [
  {
    name: "finite verb extra",
    tag: "V-PAI-3S-M",
    expected: {
      "Part of Speech": "Verb",
      Tense: "Present",
      Voice: "Active",
      Mood: "Indicative",
      Person: "Third Person",
      Number: "Singular",
      "Verb Extra": "Middle significance",
    },
  },
  {
    name: "contracted form in verb context",
    tag: "V-PAI-3S-C",
    expected: {
      "Part of Speech": "Verb",
      Tense: "Present",
      Voice: "Active",
      Mood: "Indicative",
      Person: "Third Person",
      Number: "Singular",
      "Verb Extra": "Contracted form",
    },
  },
  {
    name: "infinitive modifier without person or number",
    tag: "V-RAN-ATT",
    expected: {
      "Part of Speech": "Verb",
      Tense: "Perfect",
      Voice: "Active",
      Mood: "Infinitive",
      "Verb Extra": "Attic",
    },
  },
  {
    name: "verb suffix",
    tag: "V-PAI-3S-K",
    expected: {
      "Part of Speech": "Verb",
      Tense: "Present",
      Voice: "Active",
      Mood: "Indicative",
      Person: "Third Person",
      Number: "Singular",
      Suffix: "Crasis",
    },
  },
  {
    name: "personal pronoun",
    tag: "P-1NS",
    expected: {
      "Part of Speech": "Personal Pronoun",
      Person: "First Person",
      Case: "Nominative",
      Number: "Singular",
    },
  },
];

async function decode(page, decoderPath, tag) {
  await page.goto(decoderPath);
  await page.getByLabel("Parsing Tag:").fill(tag);
  await page.getByRole("button", { name: "Decode" }).click();
  return JSON.parse(await page.locator("#decodedOutput").innerText());
}

for (const decoderPage of decoderPages) {
  test.describe(decoderPage.name, () => {
    for (const decodingCase of decodingCases) {
      test(`decodes ${decodingCase.name}`, async ({ page }) => {
        const output = await decode(page, decoderPage.path, decodingCase.tag);
        expect(output).toEqual(decodingCase.expected);
      });
    }

    test("normalizes whitespace and lowercase input", async ({ page }) => {
      const output = await decode(page, decoderPage.path, "  v-ran-att  ");
      expect(output["Verb Extra"]).toBe("Attic");
      expect(output).not.toHaveProperty("Person");
      expect(output).not.toHaveProperty("Number");
      expect(output).not.toHaveProperty("Suffix");
    });

    test("shows a message for empty input", async ({ page }) => {
      await page.goto(decoderPage.path);
      await page.getByRole("button", { name: "Decode" }).click();
      await expect(page.locator("#decodedOutput")).toHaveText(
        "Please enter a parsing tag.",
      );
    });

    test("reports unsupported tags", async ({ page }) => {
      const output = await decode(page, decoderPage.path, "UNKNOWN");
      expect(output).toEqual({ "Part of Speech": "Unknown or Unsupported" });
    });
  });
}
