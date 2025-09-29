"""
Comprehensive Ayurvedic Body Types and Vedic Astrology Knowledge Base
Integrating Dr. Helen Thomas DC's 44 years of clinical experience
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class AyurvedaAstrologyKB:
    """Knowledge base for Ayurvedic constitutions and Vedic astrology"""
    
    def __init__(self):
        self.thirteen_constitutions = self._load_thirteen_constitutions()
        self.planetary_influences = self._load_planetary_influences()
        self.seasonal_guidance = self._load_seasonal_guidance()
        self.life_stage_wisdom = self._load_life_stage_wisdom()
        self.clinical_protocols = self._load_clinical_protocols()
    
    def _load_thirteen_constitutions(self) -> Dict:
        """The 13 Ayurvedic body types with detailed characteristics"""
        return {
            "vata": {
                "primary_qualities": ["dry", "light", "cold", "rough", "subtle", "mobile"],
                "physical_traits": {
                    "body_type": "Thin, light frame, prominent joints",
                    "skin": "Dry, rough, cool to touch, darker complexion",
                    "hair": "Dry, brittle, curly or kinky",
                    "eyes": "Small, dry, active, brown or black",
                    "appetite": "Variable, irregular eating patterns",
                    "digestion": "Irregular, gas, bloating, constipation",
                    "sleep": "Light, interrupted, 5-7 hours"
                },
                "mental_traits": {
                    "personality": "Creative, enthusiastic, quick thinking",
                    "emotions": "Anxious when stressed, fearful, worried",
                    "learning": "Quick to learn, quick to forget",
                    "speech": "Fast, talkative, interrupts others"
                },
                "imbalance_signs": [
                    "Anxiety, restlessness, insomnia",
                    "Constipation, gas, bloating",
                    "Dry skin, brittle nails",
                    "Joint pain, muscle tension",
                    "Irregular appetite and digestion"
                ],
                "balancing_foods": [
                    "Warm, moist, oily foods",
                    "Sweet, sour, salty tastes",
                    "Cooked grains, root vegetables",
                    "Warm milk, ghee, nuts",
                    "Avoid cold, dry, raw foods"
                ],
                "lifestyle_recommendations": [
                    "Regular daily routine",
                    "Warm oil massage (abhyanga)",
                    "Gentle, grounding exercises",
                    "Early bedtime, adequate rest",
                    "Meditation and breathing practices"
                ],
                "herbs": ["Ashwagandha", "Brahmi", "Jatamansi", "Bala", "Shatavari"]
            },
            
            "pitta": {
                "primary_qualities": ["hot", "sharp", "light", "oily", "liquid", "mobile"],
                "physical_traits": {
                    "body_type": "Medium build, good muscle development",
                    "skin": "Warm, oily, soft, fair or reddish",
                    "hair": "Fine, soft, early graying or balding",
                    "eyes": "Sharp, penetrating, light colored",
                    "appetite": "Strong, regular, gets angry when hungry",
                    "digestion": "Strong, efficient, prone to acidity",
                    "sleep": "Sound, moderate, 6-8 hours"
                },
                "mental_traits": {
                    "personality": "Intelligent, focused, competitive",
                    "emotions": "Irritable when stressed, angry, critical",
                    "learning": "Sharp intellect, good memory",
                    "speech": "Precise, articulate, convincing"
                },
                "imbalance_signs": [
                    "Anger, irritability, criticism",
                    "Heartburn, acid reflux, ulcers",
                    "Skin rashes, inflammation",
                    "Excessive heat, sweating",
                    "Perfectionism, impatience"
                ],
                "balancing_foods": [
                    "Cool, sweet, bitter foods",
                    "Fresh fruits, leafy greens",
                    "Coconut, cucumber, melons",
                    "Avoid spicy, sour, salty foods",
                    "Room temperature or cool drinks"
                ],
                "lifestyle_recommendations": [
                    "Avoid excessive heat and sun",
                    "Cooling practices and environments",
                    "Moderate exercise, avoid overexertion",
                    "Stress management techniques",
                    "Regular meals, don't skip eating"
                ],
                "herbs": ["Amalaki", "Neem", "Aloe Vera", "Brahmi", "Shatavari"]
            },
            
            "kapha": {
                "primary_qualities": ["heavy", "slow", "cold", "oily", "smooth", "stable"],
                "physical_traits": {
                    "body_type": "Large, heavy frame, gains weight easily",
                    "skin": "Thick, oily, smooth, pale",
                    "hair": "Thick, wavy, lustrous, oily",
                    "eyes": "Large, calm, blue or brown",
                    "appetite": "Slow, steady, can skip meals",
                    "digestion": "Slow, heavy feeling after eating",
                    "sleep": "Deep, long, 8+ hours, hard to wake"
                },
                "mental_traits": {
                    "personality": "Calm, steady, compassionate",
                    "emotions": "Depressed when stressed, attached",
                    "learning": "Slow to learn, excellent retention",
                    "speech": "Slow, melodious, few words"
                },
                "imbalance_signs": [
                    "Weight gain, sluggishness",
                    "Depression, lethargy",
                    "Congestion, mucus production",
                    "Attachment, possessiveness",
                    "Resistance to change"
                ],
                "balancing_foods": [
                    "Light, warm, spicy foods",
                    "Pungent, bitter, astringent tastes",
                    "Vegetables, legumes, spices",
                    "Avoid heavy, oily, sweet foods",
                    "Warm drinks, herbal teas"
                ],
                "lifestyle_recommendations": [
                    "Regular vigorous exercise",
                    "Dry brushing, saunas",
                    "Stimulating activities",
                    "Avoid daytime naps",
                    "Embrace change and variety"
                ],
                "herbs": ["Trikatu", "Guggulu", "Punarnava", "Chitrak", "Bibhitaki"]
            },
            
            # Dual constitutions
            "vata-pitta": {
                "characteristics": "Variable appetite, creative but focused, sensitive to both cold and heat",
                "balancing_approach": "Emphasize sweet taste, regular routine with flexibility",
                "seasonal_care": "Extra attention during fall (vata season) and summer (pitta season)"
            },
            
            "pitta-vata": {
                "characteristics": "Strong digestion with irregular appetite, intense but changeable",
                "balancing_approach": "Cool, grounding foods, stress management crucial",
                "seasonal_care": "Summer and fall require special attention"
            },
            
            "pitta-kapha": {
                "characteristics": "Strong build with good digestion, can be intense but stable",
                "balancing_approach": "Moderate approach, avoid extremes in temperature",
                "seasonal_care": "Summer and spring need attention"
            },
            
            "kapha-pitta": {
                "characteristics": "Solid build with strong appetite, steady but can be stubborn",
                "balancing_approach": "Light, warm foods, regular exercise",
                "seasonal_care": "Spring and summer focus"
            },
            
            "vata-kapha": {
                "characteristics": "Variable energy, can be both anxious and lethargic",
                "balancing_approach": "Warm, nourishing foods, gentle routine",
                "seasonal_care": "Fall and spring require balance"
            },
            
            "kapha-vata": {
                "characteristics": "Generally stable but with periods of anxiety",
                "balancing_approach": "Consistent routine, warm environment",
                "seasonal_care": "Winter and fall need attention"
            },
            
            # Triple constitution (rare)
            "vata-pitta-kapha": {
                "characteristics": "Balanced constitution, adaptable but needs attention to all three doshas",
                "balancing_approach": "Seasonal adjustments, listen to body's needs",
                "seasonal_care": "Adjust practices with each season"
            },
            
            # Additional constitutional variations
            "vata-predominant": {
                "characteristics": "Strong vata with secondary dosha influence",
                "focus": "Grounding and routine while addressing secondary dosha"
            },
            
            "pitta-predominant": {
                "characteristics": "Strong pitta with secondary dosha influence", 
                "focus": "Cooling and moderation while balancing secondary dosha"
            }
        }
    
    def _load_planetary_influences(self) -> Dict:
        """Vedic astrology planetary influences on health and constitution"""
        return {
            "sun": {
                "ayurvedic_correlation": "Pitta dosha",
                "body_parts": ["heart", "eyes", "head", "bones"],
                "health_influences": {
                    "positive": "Strong digestion, leadership, vitality, confidence",
                    "negative": "Heart problems, eye issues, fever, ego problems"
                },
                "constitutional_impact": "Increases fire element, enhances pitta qualities",
                "remedial_measures": [
                    "Offer water to Sun at sunrise",
                    "Chant Gayatri mantra",
                    "Wear ruby (if suitable)",
                    "Practice Surya Namaskara"
                ],
                "dietary_guidance": "Cooling foods during strong Sun periods"
            },
            
            "moon": {
                "ayurvedic_correlation": "Kapha dosha",
                "body_parts": ["mind", "chest", "stomach", "reproductive organs"],
                "health_influences": {
                    "positive": "Emotional stability, good memory, nurturing nature",
                    "negative": "Mental instability, water retention, digestive issues"
                },
                "constitutional_impact": "Increases water element, enhances kapha qualities",
                "remedial_measures": [
                    "Fast on Mondays",
                    "Chant Om Namah Shivaya",
                    "Wear pearl or moonstone",
                    "Practice meditation"
                ],
                "dietary_guidance": "Light foods during full moon, nourishing during new moon"
            },
            
            "mars": {
                "ayurvedic_correlation": "Pitta dosha",
                "body_parts": ["blood", "muscles", "bone marrow", "genitals"],
                "health_influences": {
                    "positive": "Strong immunity, courage, physical strength",
                    "negative": "Blood disorders, inflammation, accidents, anger"
                },
                "constitutional_impact": "Increases fire and earth elements",
                "remedial_measures": [
                    "Chant Hanuman Chalisa",
                    "Donate red lentils on Tuesdays",
                    "Wear red coral",
                    "Practice martial arts or vigorous exercise"
                ],
                "dietary_guidance": "Cooling, sweet foods to balance Mars heat"
            },
            
            "mercury": {
                "ayurvedic_correlation": "All three doshas (tridoshic)",
                "body_parts": ["nervous system", "skin", "lungs", "speech organs"],
                "health_influences": {
                    "positive": "Sharp intellect, good communication, adaptability",
                    "negative": "Nervous disorders, skin problems, speech issues"
                },
                "constitutional_impact": "Enhances mental faculties, affects all doshas",
                "remedial_measures": [
                    "Chant Vishnu mantras",
                    "Donate green items on Wednesdays",
                    "Wear emerald",
                    "Practice pranayama"
                ],
                "dietary_guidance": "Sattvic foods to enhance mental clarity"
            },
            
            "jupiter": {
                "ayurvedic_correlation": "Kapha dosha",
                "body_parts": ["liver", "pancreas", "thighs", "brain"],
                "health_influences": {
                    "positive": "Wisdom, good judgment, healthy liver function",
                    "negative": "Diabetes, liver problems, obesity, lack of wisdom"
                },
                "constitutional_impact": "Increases water and earth elements",
                "remedial_measures": [
                    "Chant Guru mantras",
                    "Donate yellow items on Thursdays",
                    "Wear yellow sapphire",
                    "Study spiritual texts"
                ],
                "dietary_guidance": "Moderate, sattvic diet, avoid excess sweets"
            },
            
            "venus": {
                "ayurvedic_correlation": "Kapha and Pitta",
                "body_parts": ["reproductive organs", "kidneys", "face", "throat"],
                "health_influences": {
                    "positive": "Beauty, creativity, harmonious relationships",
                    "negative": "Reproductive issues, kidney problems, indulgence"
                },
                "constitutional_impact": "Enhances water element and beauty",
                "remedial_measures": [
                    "Chant Lakshmi mantras",
                    "Donate white items on Fridays",
                    "Wear diamond or white sapphire",
                    "Practice artistic activities"
                ],
                "dietary_guidance": "Balanced, beautiful foods, avoid excess dairy"
            },
            
            "saturn": {
                "ayurvedic_correlation": "Vata dosha",
                "body_parts": ["bones", "joints", "teeth", "nervous system"],
                "health_influences": {
                    "positive": "Discipline, longevity, spiritual growth",
                    "negative": "Joint problems, depression, chronic diseases"
                },
                "constitutional_impact": "Increases air and space elements",
                "remedial_measures": [
                    "Chant Shani mantras",
                    "Donate black items on Saturdays",
                    "Wear blue sapphire (with caution)",
                    "Practice yoga and meditation"
                ],
                "dietary_guidance": "Warm, nourishing foods, regular meal times"
            },
            
            "rahu": {
                "ayurvedic_correlation": "Vata dosha (shadow planet)",
                "body_parts": ["nervous system", "skin", "lungs"],
                "health_influences": {
                    "positive": "Innovation, research abilities, foreign connections",
                    "negative": "Mental confusion, skin diseases, respiratory issues"
                },
                "constitutional_impact": "Disturbs natural rhythms, increases vata",
                "remedial_measures": [
                    "Chant Rahu mantras",
                    "Donate blue/black items",
                    "Wear hessonite garnet",
                    "Practice grounding exercises"
                ],
                "dietary_guidance": "Simple, pure foods, avoid processed foods"
            },
            
            "ketu": {
                "ayurvedic_correlation": "Pitta dosha (shadow planet)",
                "body_parts": ["abdomen", "spine", "nervous system"],
                "health_influences": {
                    "positive": "Spiritual insight, detachment, healing abilities",
                    "negative": "Digestive issues, spine problems, mental instability"
                },
                "constitutional_impact": "Creates spiritual fire, can disturb pitta",
                "remedial_measures": [
                    "Chant Ketu mantras",
                    "Donate multi-colored items",
                    "Wear cat's eye",
                    "Practice spiritual disciplines"
                ],
                "dietary_guidance": "Cooling, spiritual foods, avoid meat and alcohol"
            }
        }
    
    def _load_seasonal_guidance(self) -> Dict:
        """Seasonal recommendations for different constitutions"""
        return {
            "spring": {
                "dominant_dosha": "kapha",
                "general_guidance": "Time for cleansing and renewal",
                "vata_care": "Gentle cleansing, warm foods, avoid cold",
                "pitta_care": "Moderate cleansing, bitter tastes, avoid heating",
                "kapha_care": "Strong detox, spicy foods, vigorous exercise",
                "foods_to_favor": ["bitter greens", "spices", "light foods"],
                "foods_to_avoid": ["heavy", "sweet", "oily foods"],
                "lifestyle": ["spring cleaning", "new projects", "exercise increase"],
                "herbs": ["Triphala", "Trikatu", "Dandelion", "Nettle"]
            },
            
            "summer": {
                "dominant_dosha": "pitta",
                "general_guidance": "Time for cooling and moderation",
                "vata_care": "Stay hydrated, avoid excessive heat",
                "pitta_care": "Cooling foods, avoid anger, moderate activity",
                "kapha_care": "Light foods, avoid ice, maintain activity",
                "foods_to_favor": ["sweet fruits", "cooling herbs", "coconut"],
                "foods_to_avoid": ["spicy", "sour", "salty foods"],
                "lifestyle": ["early morning activities", "cooling practices", "swimming"],
                "herbs": ["Aloe", "Rose", "Coriander", "Fennel"]
            },
            
            "fall": {
                "dominant_dosha": "vata",
                "general_guidance": "Time for grounding and nourishment",
                "vata_care": "Warm, oily foods, regular routine, oil massage",
                "pitta_care": "Sweet, grounding foods, avoid dryness",
                "kapha_care": "Warm, light foods, maintain activity",
                "foods_to_favor": ["root vegetables", "warm grains", "ghee"],
                "foods_to_avoid": ["cold", "dry", "raw foods"],
                "lifestyle": ["consistent routine", "warm baths", "gentle exercise"],
                "herbs": ["Ashwagandha", "Bala", "Sesame oil", "Ginger"]
            },
            
            "winter": {
                "dominant_dosha": "vata and kapha",
                "general_guidance": "Time for building strength and immunity",
                "vata_care": "Heavy, warm, oily foods, stay warm",
                "pitta_care": "Warming foods, maintain digestive fire",
                "kapha_care": "Spicy, light foods, avoid excess sleep",
                "foods_to_favor": ["warming spices", "hot soups", "nuts"],
                "foods_to_avoid": ["cold drinks", "ice cream", "raw foods"],
                "lifestyle": ["indoor activities", "oil massage", "warm clothing"],
                "herbs": ["Chyavanprash", "Ginger", "Cinnamon", "Cloves"]
            }
        }
    
    def _load_life_stage_wisdom(self) -> Dict:
        """Life stage recommendations based on Ayurvedic principles"""
        return {
            "childhood": {
                "age_range": "0-16 years",
                "dominant_dosha": "kapha",
                "characteristics": "Growth, development, building immunity",
                "dietary_needs": "Nourishing, building foods, warm milk, ghee",
                "lifestyle": "Regular routine, adequate sleep, play",
                "common_issues": "Respiratory congestion, digestive issues",
                "herbs": "Gentle herbs like honey, ghee, mild spices"
            },
            
            "youth": {
                "age_range": "16-50 years", 
                "dominant_dosha": "pitta",
                "characteristics": "Achievement, career, family building",
                "dietary_needs": "Balanced nutrition, regular meals, cooling foods",
                "lifestyle": "Balanced work-life, stress management, exercise",
                "common_issues": "Stress, digestive fire imbalance, skin issues",
                "herbs": "Brahmi, Shankhpushpi, Amalaki, Shatavari"
            },
            
            "maturity": {
                "age_range": "50+ years",
                "dominant_dosha": "vata",
                "characteristics": "Wisdom, spiritual growth, body maintenance",
                "dietary_needs": "Warm, nourishing, easy to digest foods",
                "lifestyle": "Gentle exercise, meditation, regular routine",
                "common_issues": "Joint problems, memory issues, insomnia",
                "herbs": "Ashwagandha, Brahmi, Guggulu, Triphala"
            }
        }
    
    def _load_clinical_protocols(self) -> Dict:
        """Dr. Helen's clinical protocols from 44 years of practice"""
        return {
            "pulse_diagnosis": {
                "vata_pulse": "Moves like a snake - irregular, thin, fast",
                "pitta_pulse": "Moves like a frog - jumping, strong, regular",
                "kapha_pulse": "Moves like a swan - slow, steady, deep"
            },
            
            "tongue_diagnosis": {
                "vata_tongue": "Dry, rough, cracked, brownish coating",
                "pitta_tongue": "Red, inflamed, yellow coating",
                "kapha_tongue": "Pale, thick, white coating, swollen"
            },
            
            "treatment_protocols": {
                "vata_disorders": {
                    "primary_treatment": "Oil therapies, warm treatments",
                    "herbs": "Ashwagandha, Bala, Dashamoola",
                    "lifestyle": "Regular routine, warm environment",
                    "duration": "3-6 months for chronic conditions"
                },
                "pitta_disorders": {
                    "primary_treatment": "Cooling therapies, bitter herbs",
                    "herbs": "Amalaki, Neem, Brahmi",
                    "lifestyle": "Avoid heat, practice moderation",
                    "duration": "2-4 months typically"
                },
                "kapha_disorders": {
                    "primary_treatment": "Stimulating therapies, detox",
                    "herbs": "Trikatu, Guggulu, Punarnava",
                    "lifestyle": "Active lifestyle, avoid heavy foods",
                    "duration": "4-8 months for weight issues"
                }
            }
        }
    
    def get_constitutional_analysis(self, constitution: str, symptoms: List[str] = None) -> Dict:
        """Provide detailed constitutional analysis"""
        if constitution.lower() not in self.thirteen_constitutions:
            return {"error": "Constitution not found"}
        
        const_data = self.thirteen_constitutions[constitution.lower()]
        
        analysis = {
            "constitution": constitution,
            "primary_qualities": const_data.get("primary_qualities", []),
            "physical_traits": const_data.get("physical_traits", {}),
            "mental_traits": const_data.get("mental_traits", {}),
            "imbalance_signs": const_data.get("imbalance_signs", []),
            "balancing_foods": const_data.get("balancing_foods", []),
            "lifestyle_recommendations": const_data.get("lifestyle_recommendations", []),
            "recommended_herbs": const_data.get("herbs", [])
        }
        
        # Add symptom analysis if provided
        if symptoms:
            analysis["symptom_analysis"] = self._analyze_symptoms(constitution, symptoms)
        
        return analysis
    
    def get_planetary_guidance(self, planet: str, constitution: str = None) -> Dict:
        """Provide planetary influence guidance"""
        if planet.lower() not in self.planetary_influences:
            return {"error": "Planet not found"}
        
        planet_data = self.planetary_influences[planet.lower()]
        
        guidance = {
            "planet": planet,
            "ayurvedic_correlation": planet_data["ayurvedic_correlation"],
            "body_parts_governed": planet_data["body_parts"],
            "health_influences": planet_data["health_influences"],
            "constitutional_impact": planet_data["constitutional_impact"],
            "remedial_measures": planet_data["remedial_measures"],
            "dietary_guidance": planet_data["dietary_guidance"]
        }
        
        # Add constitutional specific guidance if provided
        if constitution:
            guidance["constitutional_specific"] = self._get_planetary_constitutional_guidance(planet, constitution)
        
        return guidance
    
    def get_seasonal_recommendations(self, season: str, constitution: str) -> Dict:
        """Get seasonal recommendations for specific constitution"""
        if season.lower() not in self.seasonal_guidance:
            return {"error": "Season not found"}
        
        season_data = self.seasonal_guidance[season.lower()]
        const_key = f"{constitution.lower()}_care"
        
        recommendations = {
            "season": season,
            "dominant_dosha": season_data["dominant_dosha"],
            "general_guidance": season_data["general_guidance"],
            "constitutional_care": season_data.get(const_key, "General care applies"),
            "foods_to_favor": season_data["foods_to_favor"],
            "foods_to_avoid": season_data["foods_to_avoid"],
            "lifestyle_recommendations": season_data["lifestyle"],
            "seasonal_herbs": season_data["herbs"]
        }
        
        return recommendations
    
    def _analyze_symptoms(self, constitution: str, symptoms: List[str]) -> Dict:
        """Analyze symptoms in context of constitution"""
        # This would contain Dr. Helen's clinical analysis patterns
        symptom_analysis = {
            "constitutional_correlation": "Analyzing symptoms in context of " + constitution,
            "likely_imbalances": [],
            "recommended_approach": [],
            "clinical_notes": "Based on 44 years of clinical experience"
        }
        
        # Add specific symptom analysis logic here
        return symptom_analysis
    
    def _get_planetary_constitutional_guidance(self, planet: str, constitution: str) -> Dict:
        """Get planet-specific guidance for constitution"""
        return {
            "interaction": f"How {planet} affects {constitution} constitution",
            "specific_recommendations": f"Tailored guidance for {constitution} during {planet} periods",
            "clinical_experience": "Dr. Helen's observations on this combination"
        }

# Initialize the knowledge base
ayurveda_astrology_kb = AyurvedaAstrologyKB()
