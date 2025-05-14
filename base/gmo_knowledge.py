GMO_KNOWLEDGE = {
    "gmo_basics": """
        Genetically Modified Organisms (GMOs) are organisms whose genetic material has been altered using genetic engineering techniques. 
        This technology allows for the introduction of new traits or enhancement of existing characteristics in plants, animals, and microorganisms.
        In agriculture, GMOs are primarily used to improve crop yields, enhance nutritional content, increase drought tolerance, 
        and provide resistance to pests and diseases.
    """,
    "regulations": """
        In the United States, three federal agencies regulate GMOs:
        1. FDA - Ensures food safety
        2. USDA - Oversees plant health and environmental safety
        3. EPA - Regulates pesticide use in GMO plants
        The approval process typically takes 5-7 years and involves extensive testing for:
        - Food safety
        - Environmental impact
        - Efficacy claims
    """,
    "crops": """
        Common GMO crops and their adoption rates in the US (2023):
        - Corn: 92% of acreage
        - Soybeans: 94% of acreage
        - Cotton: 96% of acreage
        - Canola: 95% of acreage
        These crops are primarily modified for:
        - Insect resistance (Bt traits)
        - Herbicide tolerance
        - Drought resistance
    """,
    "verification": """
        To verify GMO seeds or products:
        1. Check for certification tags or labels
        2. Look for a unique identifier code (usually a QR code)
        3. Verify through the manufacturer's database
        4. Consult the USDA's Bioengineered Food Disclosure list
        5. Use approved testing kits for field verification
    """,
    "safety": """
        Scientific consensus on GMO safety:
        - Over 2,800 independent studies have found GMOs to be as safe as conventional crops
        - Major health organizations (WHO, AMA, AAAS) endorse their safety
        - Longest study: 10-year multi-generational study showing no adverse effects
        Potential benefits:
        - Reduced pesticide use (37% decrease)
        - Increased yields (22% average increase)
        - Enhanced nutrition (Golden Rice with Vitamin A)
    """,
    
    "science": """
Genetically Modified Organisms (GMOs) are living organisms whose genetic material has been artificially manipulated through genetic engineering. 
This typically involves the insertion of genes from another organism to introduce desired traits. Key scientific aspects:
- DNA is extracted from a donor organism with desired traits
- Target genes are isolated and inserted into the host plant's genome
- Common modifications include pest resistance (Bt crops), herbicide tolerance (Roundup Ready), and improved nutrition (Golden Rice)
- The process is more precise than traditional breeding but still faces scientific debates about long-term effects
""",
    
    "regulations": """
GMO regulations vary significantly by country:
United States:
- FDA, USDA, and EPA jointly regulate GMOs
- Generally product-based (focus on the final product rather than process)
- Mandatory labeling required for foods with detectable modified genetic material

European Union:
- Process-based regulation (any genetic modification triggers regulation)
- Strict pre-market approval required
- All GMO foods must be labeled regardless of detectability

Africa:
- Varies by country - South Africa and Nigeria are most GMO-friendly
- Many countries have strict bans or moratoriums
- African Union developing harmonized guidelines

Asia:
- China has strict controls but invests heavily in GMO research
- India allows Bt cotton but has contentious debates about food crops
""",
    
    "crops": """
Major GMO Crops and Their Modifications:
1. Corn (Maize):
   - 80% of US corn is GMO
   - Traits: Insect resistance (Bt corn), herbicide tolerance, drought resistance
   - Uses: Animal feed, ethanol, processed foods

2. Soybeans:
   - 94% of US soybeans are GMO
   - Primarily modified for herbicide tolerance
   - Used in animal feed, vegetable oil, and food additives

3. Cotton:
   - Primarily Bt cotton for pest resistance
   - Accounts for 80% of global cotton production
   - Also modified for improved fiber quality

4. Canola:
   - Herbicide-tolerant varieties dominate
   - Mainly used for vegetable oil and biofuels

5. Newer Developments:
   - Golden Rice (Vitamin A enriched)
   - Non-browning Arctic Apples
   - Late Blight-resistant Potatoes
""",
    
    "verification": """
How to Verify GMO Status:
1. Label Checking:
   - Look for "Bioengineered" label (US)
   - EU uses "Genetically Modified" label
   - Non-GMO Project Verified seal for non-GMO products

2. Testing Methods:
   - PCR (Polymerase Chain Reaction) tests can detect GMO DNA
   - Protein-based test strips for common modifications
   - Laboratory analysis for comprehensive verification

3. Documentation:
   - Request seed certification documents from suppliers
   - Check for compliance with local GMO regulations
   - Traceability systems in regulated markets

4. Organic Certification:
   - USDA Organic and EU Organic prohibit GMO use
   - Requires audit trails to prevent contamination
""",
    
    "myths": """
Common GMO Myths vs Facts:
Myth 1: GMOs cause cancer
Fact: No credible evidence links GMO consumption to cancer. All approved GMOs undergo rigorous safety testing.

Myth 2: GMOs are unnatural
Fact: Genetic modification is an extension of traditional breeding, just more precise. Many natural organisms also perform horizontal gene transfer.

Myth 3: GMOs harm bees and butterflies
Fact: While some pesticides used with GMO crops can affect pollinators, the GMOs themselves aren't the primary issue. Newer GMOs actually reduce pesticide use.

Myth 4: GMOs don't increase yields
Fact: Yield gains vary by crop and environment, but pest-resistant varieties often show significant yield improvements, especially in developing countries.

Myth 5: GMO companies sue farmers for accidental contamination
Fact: No cases exist of lawsuits over accidental contamination. Cases involve deliberate patent violations.
"""

}



def get_related_suggestions(topic=None):
    """Get context-aware suggestions"""
    if topic == 'regulations':
        return ["US GMO regulations", "EU GMO laws", "African GMO policies"]
    elif topic == 'crops':
        return ["GMO cotton benefits", "Soybean modifications", "Golden rice nutrition"]
    return [
        "GMO regulations in my area",
        "How to verify seed authenticity",
        "Benefits of GMO corn",
        "Non-GMO alternatives"
    ]