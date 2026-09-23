**BIS Category Taxonomy — For Babar's AI Engine**

*SIH 2026 · Problem ID SIH26108 · Prepared by Ilha & Basit*

This is a practical, 12-category list built from the standards we
actually collected (File 02 / File 07) — not an invented or theoretical
taxonomy. It is deliberately simple: 12 categories, each with a one-line
description, typical procurement terms, and real example standards.

How Babar should use categories

- Metadata filter (recommended default): store category as a field on
  each record and let the backend/frontend filter or narrow results by
  it. This does NOT require re-training or touching the embedding model.

- Optional query hint: if a user's search box includes a category
  dropdown (Dayan's UI mentions this), pass the selected category to the
  backend as a filter parameter alongside the text query — apply it
  before or after the FAISS similarity search, whichever is simpler to
  wire up first.

- Not required in the embedding text by default: category names are
  short and somewhat generic (e.g. “Construction & Building Materials”),
  so embedding them adds little semantic signal compared to title +
  description + keywords. Only add category into embedding_text if early
  testing (Aatif's sample queries) shows the AI engine confusing
  standards across very different sectors.

- Not a fixed/rigid taxonomy: as more standards get added (see File 05,
  “What I still need to confirm”), a category may need to split into
  two, or a new category may be needed. Treat this list as versioned,
  not frozen.

Category List

**1. Construction & Building Materials**

Description: Standards governing concrete, cement, plywood and general
construction materials (not raw/structural steel itself — see next
category).

*Typical procurement terms/keywords: concrete, cement, RCC, PCC,
plywood, shuttering, construction materials*

Example standards from our dataset: IS 456:2000, IS 269:2015, IS
4990:2011

**2. Structural & Constructional Steel**

Description: Standards for structural/reinforcement steel products and
their raw materials (billets, bars, sections).

*Typical procurement terms/keywords: structural steel, TMT bars, rebar,
billets, hot rolled steel*

Example standards from our dataset: IS 2062:2011, IS 1786:2008, IS
2830:2012

**3. Electrical Appliances & Household Safety**

Description: General and appliance-specific safety standards for
household and similar electrical appliances.

*Typical procurement terms/keywords: household appliances, electrical
safety, IEC 60335*

Example standards from our dataset: IS 302 (Part 1):2024

**4. Lighting & LED Products**

Description: Standards for LED lamps, modules and related lighting
products.

*Typical procurement terms/keywords: LED, lighting, lamps, luminaires*

Example standards from our dataset: IS 16102 (Part 1):2012

**5. Electrical Machines & Cables**

Description: Standards for rotating electrical machines
(motors/generators) and electrical wiring/cables.

*Typical procurement terms/keywords: motors, generators, cables, wiring,
rotating machines*

Example standards from our dataset: IS 4722:2001, IS 694:2010

**6. IT & Electronics Equipment Safety**

Description: Safety standards for information technology and electronics
equipment.

*Typical procurement terms/keywords: IT equipment, electronics safety,
IEC 60950*

Example standards from our dataset: IS 13252 (Part 1):2010

**7. Toys & Children's Product Safety**

Description: Safety standards for toys and children's products.

*Typical procurement terms/keywords: toys, child safety, ISO 8124*

Example standards from our dataset: IS 9873 (Part 1):2019

**8. Personal Protective Equipment (PPE)**

Description: Standards for personal protective equipment including
safety footwear.

*Typical procurement terms/keywords: PPE, safety footwear, industrial
safety, ISO 20345*

Example standards from our dataset: IS 15298 (Part 2):2024

**9. Household & Domestic Appliances**

Description: Product specifications for domestic/kitchen appliances
(non-electrical-safety-committee standards).

*Typical procurement terms/keywords: pressure cooker, kitchen
appliances, domestic products*

Example standards from our dataset: IS 2347:2017

**10. Drinking Water & Water Supply**

Description: Standards for drinking water quality, packaged water and
water-supply piping.

*Typical procurement terms/keywords: drinking water, potable water,
pipes, water quality*

Example standards from our dataset: IS 10500:2012, IS 14543:2016, IS
4984:2016, IS 4985:2021

**11. Food Products & Packaging**

Description: Standards for packaged food products and food/beverage
packaging materials.

*Typical procurement terms/keywords: food specification, packaging,
containers, salt*

Example standards from our dataset: IS 7224:2006, IS 15410:2003

**12. Quality Control, Sampling & Testing Methods**

Description: Cross-cutting methodology standards for sampling and
statistical quality control — referenced by many product standards
rather than describing a product themselves.

*Typical procurement terms/keywords: sampling, AQL, random sampling,
quality control, statistical methods*

Example standards from our dataset: IS 4905:2015, IS 2500 (Part 1):2000
