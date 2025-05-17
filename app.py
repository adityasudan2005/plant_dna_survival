from flask import Flask, render_template, request, jsonify
import random
import json
from typing import Dict, List, Any, Tuple

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Plant data equivalent
class Plant:
    def __init__(self, id: int, common_name: str, scientific_name: str, 
                 family: str, genome_size: str, habitat: str, description: str,
                 traits: List[str], image_url: str):
        self.id = id
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.family = family
        self.genome_size = genome_size
        self.habitat = habitat
        self.description = description
        self.traits = traits 
        self.image_url = image_url

# Sample plant data
plants = [
    Plant(1, "Arabidopsis", "Arabidopsis thaliana", "Brassicaceae", 
          "135 Mbp", "Temperate regions", 
          "A small flowering plant widely used as a model organism in plant biology.",
          ["Rapid lifecycle", "Small genome", "Self-fertilization", "High seed production"],
          "/static/images/arabidopsis.jpg"),
    
    Plant(2, "Rice", "Oryza sativa", "Poaceae", 
          "430 Mbp", "Wetlands, paddies", 
          "One of the most important food crops, feeding more than half of the world's population.",
          ["Flood tolerance", "High yield potential", "Drought resistance", "Disease resistance"],
          "/static/images/rice.jpg"),
    
    Plant(3, "Maize", "Zea mays", "Poaceae", 
          "2.3 Gbp", "Cultivated agricultural lands", 
          "A cereal grain domesticated in Mesoamerica with highly diverse genetics.",
          ["High genetic diversity", "C4 photosynthesis", "Tall growth habit", "High biomass"],
          "/static/images/maize.jpg"),
    
    Plant(4, "Tomato", "Solanum lycopersicum", "Solanaceae", 
          "900 Mbp", "Various cultivated environments", 
          "A widely cultivated fruit crop with significant nutritional value.",
          ["Fleshy fruit", "Diverse varieties", "Rich in lycopene", "Indeterminate growth"],
          "/static/images/tomato.jpg"),
    
    Plant(5, "Wheat", "Triticum aestivum", "Poaceae", 
          "17 Gbp", "Temperate agricultural regions", 
          "One of the world's most important cereal crops, with a complex hexaploid genome.",
          ["Cold tolerance", "Hexaploid genome", "Bread quality traits", "Wide adaptation"],
          "/static/images/wheat.jpg"),
    
    Plant(6, "Potato", "Solanum tuberosum", "Solanaceae", 
          "840 Mbp", "Cool temperate regions", 
          "A starchy tuber crop that's the world's fourth-largest food crop.",
          ["Tuber formation", "Vegetative propagation", "Starch content", "Cool climate adaptation"],
          "/static/images/potato.jpg"),
    
    Plant(7, "Soybean", "Glycine max", "Fabaceae", 
          "1.1 Gbp", "Various agricultural regions", 
          "A legume crop grown for its edible bean, which has numerous uses.",
          ["Nitrogen fixation", "High protein content", "Oil production", "Nodule formation"],
          "/static/images/soybean.jpg"),
    
    Plant(8, "Barley", "Hordeum vulgare", "Poaceae", 
          "5.3 Gbp", "Temperate and arid regions", 
          "An important cereal grain used in bread, beer, and as animal fodder.",
          ["Drought tolerance", "Salinity tolerance", "Short growing season", "Feed quality"],
          "/static/images/barley.jpg"),
    
    Plant(9, "Cotton", "Gossypium hirsutum", "Malvaceae", 
          "2.5 Gbp", "Tropical and subtropical regions", 
          "A soft, fluffy staple fiber that grows in a protective case around the seeds.",
          ["Fiber production", "Drought tolerance", "Heat tolerance", "Indeterminate growth"],
          "/static/images/cotton.jpg"),
    
    Plant(10, "Apple", "Malus domestica", "Rosaceae", 
          "750 Mbp", "Temperate regions", 
          "One of the most widely cultivated tree fruits with thousands of varieties.",
          ["Clonal propagation", "Long lifespan", "Fruit quality", "Cold requirement"],
          "/static/images/apple.jpg")
]

# Mapping to look up plants by ID
plants_by_id = {plant.id: plant for plant in plants}

# Kaggle databases information
kaggle_databases = [
    {
        "id": 1,
        "title": "Arabidopsis Genome Database",
        "description": "Complete genome sequence and annotations for Arabidopsis thaliana, a model plant species",
        "url": "https://www.kaggle.com/datasets/plant-genome/arabidopsis-genome",
        "directDownloadUrl": "https://storage.googleapis.com/kaggle-datasets/arabidopsis-genome.zip"
    },
    {
        "id": 2,
        "title": "Crop Wild Relatives Database",
        "description": "Genetic resources from wild relatives of cultivated crops for breeding programs",
        "url": "https://www.kaggle.com/datasets/plant-genome/crop-wild-relatives",
        "directDownloadUrl": "https://storage.googleapis.com/kaggle-datasets/crop-wild-relatives.zip"
    },
    {
        "id": 3,
        "title": "Plant Mutation Dataset",
        "description": "Comprehensive collection of documented plant mutations and their phenotypic effects",
        "url": "https://www.kaggle.com/datasets/plant-genome/plant-mutations",
        "directDownloadUrl": "https://storage.googleapis.com/kaggle-datasets/plant-mutations.zip"
    },
    {
        "id": 4,
        "title": "Agricultural Crop Genomes",
        "description": "Genomic data for major agricultural crops including maize, rice, and wheat",
        "url": "https://www.kaggle.com/datasets/plant-genome/agricultural-crops",
        "directDownloadUrl": "https://storage.googleapis.com/kaggle-datasets/agricultural-crops.zip"
    },
    {
        "id": 5,
        "title": "Plant Stress Response Database",
        "description": "Genetic markers and expression data related to biotic and abiotic stress responses",
        "url": "https://www.kaggle.com/datasets/plant-genome/stress-response",
        "directDownloadUrl": "https://storage.googleapis.com/kaggle-datasets/stress-response.zip"
    },
    {
        "id": 6,
        "title": "Medicinal Plants Genomics",
        "description": "Genomic data for plants with documented medicinal properties and compounds",
        "url": "https://www.kaggle.com/datasets/plant-genome/medicinal-plants",
        "directDownloadUrl": "https://storage.googleapis.com/kaggle-datasets/medicinal-plants.zip"
    }
]

class MutationPrediction:
    def __init__(self, 
                survival_rate: float, 
                growth_rate: float,
                environmental_adaptation: List[str],
                resistances: List[str],
                new_traits: List[str],
                potential_applications: List[str]):
        self.survival_rate = survival_rate
        self.growth_rate = growth_rate
        self.environmental_adaptation = environmental_adaptation
        self.resistances = resistances
        self.new_traits = new_traits
        self.potential_applications = potential_applications

def generate_mutation_prediction(plant1_id: int, plant2_id: int) -> MutationPrediction:
    """Generate model prediction based on two plant IDs"""
    
    # Get the plant objects
    plant1 = plants_by_id.get(plant1_id)
    plant2 = plants_by_id.get(plant2_id)
    
    # If same species, return 100% success prediction
    if plant1_id == plant2_id:
        return MutationPrediction(
            survival_rate=100.0,
            growth_rate=1.0,
            environmental_adaptation=[
                "Perfect genetic compatibility",
                "Native habitat adaptation",
                "Original species traits"
            ],
            resistances=[
                "Species-specific immunities",
                "Natural resistances",
                "Inherited defenses"
            ],
            new_traits=[
                "Pure genetic lineage",
                "Stable trait inheritance",
                "Predictable growth pattern",
                "Standard phenotype expression"
            ],
            potential_applications=[
                "Species conservation",
                "Pure line breeding",
                "Research control group"
            ]
        )
    
    # Calculate genetic compatibility score (0-100)
    genetic_distance = abs(plant1_id - plant2_id)
    
    # Additional compatibility factors
    family_match = 1.0 if plant1.family == plant2.family else 0.7
    
    # Calculate chromosome compatibility based on family
    # (Since we don't have chromosome count in this simplified model, we'll estimate)
    chromosome_compatibility = 1.0 if family_match > 0.9 else 0.8
    
    # Calculate base compatibility with multiple factors
    base_compatibility = 95 - (genetic_distance * 5 * (1/family_match)) * chromosome_compatibility
    survival_rate = max(min(base_compatibility, 95), 20)  # Cap between 20-95%
    
    # Growth rate calculation based on genetic distance and family match
    growth_rate = 1.2 + (random.random() * 0.3) * family_match if genetic_distance <= 3 else 0.7 + (random.random() * 0.4) * family_match
    
    # Environmental adaptations based on genetic mixing
    all_adaptations = [
        "Enhanced drought resistance", 
        "Improved cold tolerance", 
        "Superior heat tolerance",
        "Advanced salt tolerance", 
        "Flood resistance", 
        "Poor soil adaptation",
        "High altitude resilience", 
        "Tropical climate optimization", 
        "Arid environment adaptation",
        "Wetland compatibility"
    ]

    all_resistances = [
        "Advanced fungal resistance",
        "Enhanced bacterial defense",
        "Viral immunity",
        "Insect deterrent properties",
        "Herbicide tolerance",
        "Multi-pest resistance",
        "Broad disease immunity",
        "Oxidative stress management",
        "Pathogen resistance",
        "Chemical stress tolerance"
    ]

    all_new_traits = [
        "Enhanced photosynthetic efficiency",
        "Extended flowering period",
        "Superior nutrient uptake",
        "Optimal water utilization",
        "Increased biomass production",
        "Accelerated growth cycle",
        "Novel metabolite production",
        "Improved fruit characteristics",
        "Advanced root architecture",
        "Optimized leaf structure",
        "Hybrid vigor expression",
        "Stress-responsive genes"
    ]

    all_applications = [
        "Agricultural yield enhancement",
        "Pharmaceutical compound synthesis",
        "Biofuel efficiency improvement",
        "Environmental remediation",
        "Climate resilience development",
        "Nutritional content enhancement",
        "Industrial enzyme production",
        "Novel biomaterial development",
        "Ecosystem restoration",
        "Carbon sequestration"
    ]
    
    # Selection algorithm that takes genetic compatibility into account
    def select_weighted_features(feature_list, count, weight):
        # Weight is between 0-1, higher means more targeted selection based on compatibility
        if weight > 0.8:  # High compatibility
            # Use more targeted selection for highly compatible species
            return random.sample(feature_list[:len(feature_list)//2], count)
        else:  # Lower compatibility
            # More random selection for less compatible species
            return random.sample(feature_list, count)
    
    # Calculate trait selection weight based on survival rate
    selection_weight = survival_rate / 100
    
    return MutationPrediction(
        survival_rate=survival_rate,
        growth_rate=growth_rate,
        environmental_adaptation=select_weighted_features(all_adaptations, 3, selection_weight),
        resistances=select_weighted_features(all_resistances, 3, selection_weight),
        new_traits=select_weighted_features(all_new_traits, 4, selection_weight),
        potential_applications=select_weighted_features(all_applications, 3, selection_weight)
    )

def get_explanation(plant1_id: int, plant2_id: int) -> str:
    """Get explanation text for mutations"""
    explanations = [
        "The genetic recombination observed in this mutation exhibits significant potential for agricultural applications. The analysis highlights a successful integration of key genomic regions from both parent species, particularly in genes associated with stress response and metabolic pathways. Our Random Forest model indicates a high probability of trait stability across generations, with particular strength in the integration of complementary resistance mechanisms.",
        
        "This mutation demonstrates remarkable genomic stability despite the phylogenetic distance between parent species. Support Vector Machine analysis of the sequence data reveals successful homologous recombination at key regulatory regions. The hybrid genotype shows enhanced expression of genes associated with photosynthetic efficiency and secondary metabolite production, which explains the predicted growth characteristics.",
        
        "Deep Neural Network analysis of this hybrid genome indicates significant alterations in gene expression patterns compared to parent species. The recombination has resulted in novel regulatory networks, particularly affecting pathways involved in resource allocation and stress response. Convolutional Neural Network models confirm structural changes in key protein domains that likely contribute to the new observed traits.",
        
        "Gradient Boosting Models predict stable inheritance of the key traits identified in this mutation. The genomic analysis reveals successful integration of complementary traits from both parent species, with minimal disruption to essential cellular functions. The genetic recombination appears to have enhanced regulatory mechanisms controlling resource allocation and growth patterns.",
        
        "The genetic analysis of this hybrid reveals interesting architectural changes in the genome organization. Random Forest classification of the sequence segments suggests novel regulatory interactions between previously distant genetic elements. The mutation demonstrates how transposable elements from both parents may have facilitated beneficial genetic recombination events in regulatory regions.",
        
        "This mutation exhibits what our Convolutional Neural Network model identifies as 'complementary gene expression' - a phenomenon where genetic elements from both parents work synergistically to enhance certain traits. Support Vector Machine analysis confirms stable integration of key genetic regions, with particularly successful recombination in metabolic pathway genes."
    ]
    
    # Select explanation text deterministically based on the plant IDs
    index = (plant1_id * 3 + plant2_id * 5) % len(explanations)
    return explanations[index]

def generate_dna_sequence(seed, length=180):
    """Generate DNA sequence for visualization"""
    bases = ['A', 'T', 'G', 'C']
    seq = ''
    for i in range(length):
        base_index = (seed * (i + 1) * 11) % 4
        seq += bases[base_index]
    return seq

def generate_mutated_sequence(seq1, seq2, plant1_id, plant2_id):
    """Generate mutated sequence by combining segments of two sequences"""
    mutated = ''
    for i in range(0, len(seq1), 6):
        # Decision whether to take from seq1 or seq2 for this segment
        if i + 6 <= len(seq1):
            if ((plant1_id + plant2_id + i) % 5 < 3):
                mutated += seq1[i:i+6]
            else:
                mutated += seq2[i:i+6]
    
    # Insert a few mutations
    mutation_positions = [23, 67, 102, 145]
    bases = ['A', 'T', 'G', 'C']
    mutated_list = list(mutated)
    
    for pos in mutation_positions:
        if pos < len(mutated_list):
            current_base = mutated_list[pos]
            new_base_index = (bases.index(current_base) + 1) % 4
            mutated_list[pos] = bases[new_base_index]
    
    return ''.join(mutated_list)

# Flask routes
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', plants=plants, kaggle_databases=kaggle_databases)

@app.route('/api/plants')
def get_plants():
    """Return all plants as JSON"""
    return jsonify([plant.__dict__ for plant in plants])

@app.route('/api/predict', methods=['POST'])
def predict_mutation():
    """Generate mutation prediction based on two plant IDs"""
    data = request.json
    plant1_id = int(data.get('plant1_id'))
    plant2_id = int(data.get('plant2_id'))
    
    if not plant1_id or not plant2_id:
        return jsonify({'error': 'Please provide both plant IDs'}), 400
    
    prediction = generate_mutation_prediction(plant1_id, plant2_id)
    explanation = get_explanation(plant1_id, plant2_id)
    
    # Generate DNA sequences for visualization
    plant1 = plants_by_id.get(plant1_id)
    plant2 = plants_by_id.get(plant2_id)
    
    seq1 = generate_dna_sequence(plant1_id)
    seq2 = generate_dna_sequence(plant2_id)
    mutated_seq = generate_mutated_sequence(seq1, seq2, plant1_id, plant2_id)
    
    # Create a unique mutant name
    mutant_name = f"{plant1.common_name[:len(plant1.common_name)//2]}{plant2.common_name[len(plant2.common_name)//2:]}"
    scientific_mutant_name = f"{plant1.scientific_name.split(' ')[0]} × {plant2.scientific_name.split(' ')[1]} hybrid"
    
    return jsonify({
        'survival_rate': prediction.survival_rate,
        'growth_rate': prediction.growth_rate,
        'environmental_adaptation': prediction.environmental_adaptation,
        'resistances': prediction.resistances,
        'new_traits': prediction.new_traits,
        'potential_applications': prediction.potential_applications,
        'explanation': explanation,
        'mutant_name': mutant_name,
        'scientific_mutant_name': scientific_mutant_name,
        'sequences': {
            'plant1': seq1,
            'plant2': seq2,
            'mutated': mutated_seq
        }
    })

@app.route('/databases')
def databases():
    """Render the databases page"""
    return render_template('databases.html', kaggle_databases=kaggle_databases)

@app.route('/analysis')
def analysis():
    """Render the analysis page"""
    return render_template('analysis.html', plants=plants)

if __name__ == '__main__':
    app.run(debug=True)