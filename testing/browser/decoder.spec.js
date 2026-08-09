const { test, expect } = require("@playwright/test");
const knownMorphTags = require("../output/morph_tags.json");

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

const validationCases = [
  {
    name: "incomplete noun",
    tag: "N-",
    errors: ["Invalid or incomplete noun tag structure"],
  },
  {
    name: "unknown noun fields",
    tag: "N-XYZ",
    errors: [
      "Unknown case value",
      "Unknown number value",
      "Unknown gender value",
      "Invalid or incomplete noun tag structure",
    ],
  },
  {
    name: "trailing noun data",
    tag: "N-NSF-GARBAGE",
    errors: ["Invalid or incomplete noun tag structure"],
  },
  {
    name: "incomplete verb",
    tag: "V-PAI",
    errors: ["Invalid or incomplete verb tag structure"],
  },
  {
    name: "trailing verb data",
    tag: "V-RAN-ATT-GARBAGE",
    errors: ["Invalid or incomplete verb tag structure"],
  },
  {
    name: "incomplete relative pronoun",
    tag: "R-NS",
    errors: ["Invalid or incomplete relative pronoun tag structure"],
  },
  {
    name: "trailing personal pronoun data",
    tag: "P-1NSM",
    errors: ["Invalid or incomplete personal pronoun tag structure"],
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

    test("decodes a morphology code supplied in the tag URL parameter", async ({ page }) => {
      const tag = encodeURIComponent("  v-ran-att  ");
      await page.goto(`${decoderPage.path}?tag=${tag}`);

      await expect(page.getByLabel("Parsing Tag:")).toHaveValue("V-RAN-ATT");
      const output = JSON.parse(await page.locator("#decodedOutput").innerText());
      expect(output).toEqual({
        "Part of Speech": "Verb",
        Tense: "Perfect",
        Voice: "Active",
        Mood: "Infinitive",
        "Verb Extra": "Attic",
      });
    });

    for (const validationCase of validationCases) {
      test(`reports ${validationCase.name}`, async ({ page }) => {
        const output = await decode(page, decoderPage.path, validationCase.tag);
        expect(output.Errors).toEqual(validationCase.errors);
      });
    }

    test("decodes every known morphology code without validation errors", async ({ page }) => {
      await page.goto(decoderPage.path);

      const failures = await page.evaluate((tags) => {
        const input = document.getElementById("tagInput");
        const output = document.getElementById("decodedOutput");

        return tags.flatMap((tag) => {
          input.value = tag;
          window.decodeTag();
          const decoded = JSON.parse(output.textContent);
          const issues = decoded.Errors || [];
          return issues.length ? [{ tag, issues }] : [];
        });
      }, knownMorphTags);

      expect(failures).toEqual([]);
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

test.describe("Python package documentation", () => {
  test("documents installation, API modes, and CLI usage", async ({ page }) => {
    await page.goto("/docs/python-package.html");

    await expect(
      page.getByRole("heading", { name: "Use the decoder as a Python package" }),
    ).toBeVisible();
    await expect(page.locator("#install")).toContainText(
      "python -m pip install sandborg-petersen-decoder",
    );
    await expect(page.locator("#modes")).toContainText("Permissive mode");
    await expect(page.locator("#modes")).toContainText("Strict mode");
    await expect(page.locator("#api")).toContainText("decode_tag");
    await expect(page.locator("#cli")).toContainText("sp-morph-decode");
  });

  test("links back to the online decoder", async ({ page }) => {
    await page.goto("/docs/python-package.html");
    await page.getByRole("link", { name: "Online decoder" }).click();
    await expect(page).toHaveURL(/\/docs\/index\.html$/);
    await expect(page.getByLabel("Parsing Tag:")).toBeVisible();
  });
});
