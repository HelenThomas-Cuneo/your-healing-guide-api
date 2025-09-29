"""
NanoSutracore - Advanced AI Engine for Ayurvedic Healing Guidance
Integrates Healing Airwaves and Ayurveda Wisdom knowledge bases
"""

import os
import json
import openai
from datetime import datetime
from typing import Dict, List, Optional, Any

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

class NanoSutracore:
    """
    Advanced AI reasoning system that combines:
    - Healing Airwaves: Dr. Helen's specialized healing methodologies
    - Ayurveda Wisdom: Traditional Ayurvedic principles and practices
    - Clinical Experience: 44 years of practical application
    """
    
    def __init__(self):
        self.healing_airwaves_kb = self._load_healing_airwaves_knowledge()
        self.ayurveda_wisdom_kb = self._load_ayurveda_wisdom_knowledge()
        self.clinical_protocols = self._load_clinical_protocols()
        
    def _load_healing_airwaves_knowledge(self) -> Dict[str, Any]:
        """Load Healing Airwaves knowledge base"""
        return {
            "core_principles": {
                "pulse_diagnosis": {
                    "description": "The pulse reveals the current state of doshas and imbalances",
                    "methodology": "Three-finger pulse reading technique to assess Vata, Pitta, Kapha",
                    "indicators": {
                        "vata_pulse": "Thin, thready, irregular, moves like a snake",
                        "pitta_pulse": "Strong, bounding, jumps like a frog", 
                        "kapha_pulse": "Slow, steady, moves like a swan"
                    }
                },
                "constitutional_analysis": {
                    "13_body_types": [
                        "Pure Vata", "Pure Pitta", "Pure Kapha",
                        "Vata-Pitta", "Vata-Kapha", "Pitta-Vata", 
                        "Pitta-Kapha", "Kapha-Vata", "Kapha-Pitta",
                        "Tri-Dosha", "Ojas-dominant", "Tejas-dominant", "Prana-dominant"
                    ],
                    "assessment_method": "Comprehensive questionnaire + pulse diagnosis + physical observation"
                },
                "healing_hierarchy": {
                    "step_1": "Identify primary imbalance through pulse and symptoms",
                    "step_2": "Address root cause: dryness, heat, or stagnation",
                    "step_3": "Apply specific protocol: moisturize, cool, or flush",
                    "step_4": "Support with appropriate herbs, diet, and lifestyle"
                }
            },
            "therapeutic_approaches": {
                "dryness_protocol": {
                    "signs": ["dry skin", "constipation", "anxiety", "insomnia", "joint pain"],
                    "treatment": "Remoisturizing with oils, warm foods, regular routine",
                    "herbs": ["ashwagandha", "sesame oil", "ghee", "dates"],
                    "lifestyle": ["oil massage", "warm baths", "consistent sleep schedule"]
                },
                "heat_protocol": {
                    "signs": ["inflammation", "anger", "acidity", "skin rashes", "burning sensation"],
                    "treatment": "Cooling with bitter herbs, sweet foods, avoiding heat",
                    "herbs": ["aloe vera", "coriander", "fennel", "coconut"],
                    "lifestyle": ["cool environments", "moderate exercise", "meditation"]
                },
                "stagnation_protocol": {
                    "signs": ["congestion", "weight gain", "lethargy", "depression", "mucus"],
                    "treatment": "Flushing with spices, light foods, vigorous exercise",
                    "herbs": ["ginger", "turmeric", "trikatu", "honey"],
                    "lifestyle": ["early rising", "dynamic movement", "stimulating activities"]
                }
            },
            "seasonal_wisdom": {
                "spring_detox": "Kapha season - focus on cleansing, light foods, exercise",
                "summer_cooling": "Pitta season - emphasize cooling foods, avoid heat",
                "fall_grounding": "Vata season - warm, nourishing foods, routine",
                "winter_building": "Kapha building - warming spices, hearty foods"
            }
        }
    
    def _load_ayurveda_wisdom_knowledge(self) -> Dict[str, Any]:
        """Load traditional Ayurveda Wisdom knowledge base"""
        return {
            "foundational_texts": {
                "charaka_samhita": "Classical text on internal medicine and constitution",
                "sushruta_samhita": "Surgical procedures and anatomical knowledge",
                "ashtanga_hridaya": "Condensed essence of Ayurvedic principles"
            },
            "panchamahabhuta": {
                "space": {"qualities": ["subtle", "light", "soft"], "functions": ["communication", "consciousness"]},
                "air": {"qualities": ["light", "dry", "mobile"], "functions": ["movement", "circulation"]},
                "fire": {"qualities": ["hot", "sharp", "light"], "functions": ["digestion", "metabolism"]},
                "water": {"qualities": ["cool", "liquid", "smooth"], "functions": ["cohesion", "lubrication"]},
                "earth": {"qualities": ["heavy", "stable", "solid"], "functions": ["structure", "support"]}
            },
            "tridosha_theory": {
                "vata": {
                    "elements": ["space", "air"],
                    "functions": ["movement", "circulation", "nervous system"],
                    "locations": ["colon", "pelvis", "bones", "skin", "ears"],
                    "imbalance_signs": ["anxiety", "insomnia", "constipation", "arthritis"]
                },
                "pitta": {
                    "elements": ["fire", "water"],
                    "functions": ["digestion", "metabolism", "intelligence"],
                    "locations": ["small intestine", "liver", "blood", "eyes", "skin"],
                    "imbalance_signs": ["anger", "inflammation", "acidity", "skin disorders"]
                },
                "kapha": {
                    "elements": ["water", "earth"],
                    "functions": ["structure", "immunity", "lubrication"],
                    "locations": ["chest", "throat", "head", "stomach", "joints"],
                    "imbalance_signs": ["congestion", "weight gain", "lethargy", "attachment"]
                }
            },
            "rasa_theory": {
                "sweet": {"elements": ["earth", "water"], "effects": "nourishing, building, calming"},
                "sour": {"elements": ["earth", "fire"], "effects": "stimulating digestion, warming"},
                "salty": {"elements": ["water", "fire"], "effects": "moistening, softening"},
                "pungent": {"elements": ["fire", "air"], "effects": "heating, drying, stimulating"},
                "bitter": {"elements": ["space", "air"], "effects": "cooling, drying, cleansing"},
                "astringent": {"elements": ["earth", "air"], "effects": "drying, contracting, healing"}
            },
            "yoga_practices": {
                "pranayama": {
                    "nadi_shodhana": "Alternate nostril breathing for balance",
                    "bhramari": "Bee breath for calming Vata",
                    "sheetali": "Cooling breath for reducing Pitta",
                    "kapalabhati": "Skull shining breath for stimulating Kapha"
                },
                "asanas": {
                    "vata_balancing": ["child's pose", "forward folds", "gentle twists"],
                    "pitta_balancing": ["moon salutation", "cooling poses", "restorative poses"],
                    "kapha_balancing": ["sun salutation", "backbends", "energizing poses"]
                }
            },
            "vedic_astrology_health": {
                "planetary_influences": {
                    "sun": {"dosha": "pitta", "organs": ["heart", "eyes"], "diseases": ["fever", "inflammation"]},
                    "moon": {"dosha": "kapha", "organs": ["mind", "stomach"], "diseases": ["mental disorders", "fluid retention"]},
                    "mars": {"dosha": "pitta", "organs": ["blood", "muscles"], "diseases": ["accidents", "blood disorders"]},
                    "mercury": {"dosha": "vata", "organs": ["nervous system", "skin"], "diseases": ["anxiety", "skin problems"]},
                    "jupiter": {"dosha": "kapha", "organs": ["liver", "fat"], "diseases": ["diabetes", "obesity"]},
                    "venus": {"dosha": "kapha", "organs": ["reproductive system"], "diseases": ["reproductive issues"]},
                    "saturn": {"dosha": "vata", "organs": ["bones", "joints"], "diseases": ["arthritis", "chronic diseases"]}
                }
            }
        }
    
    def _load_clinical_protocols(self) -> Dict[str, Any]:
        """Load Dr. Helen's 44 years of clinical protocols"""
        return {
            "assessment_protocol": {
                "initial_consultation": [
                    "Pulse diagnosis (3-5 minutes minimum)",
                    "Constitutional questionnaire",
                    "Current symptoms analysis",
                    "Lifestyle and diet assessment",
                    "Stress and emotional patterns",
                    "Sleep and energy patterns"
                ],
                "follow_up_protocol": [
                    "Pulse changes assessment",
                    "Symptom improvement tracking",
                    "Protocol adherence evaluation",
                    "Seasonal adjustments needed"
                ]
            },
            "treatment_hierarchy": {
                "acute_conditions": "Address immediate imbalance first",
                "chronic_conditions": "Build constitutional strength gradually",
                "preventive_care": "Maintain balance through seasonal adjustments"
            },
            "success_indicators": {
                "pulse_improvement": "Pulse becomes more balanced and steady",
                "symptom_reduction": "Primary complaints diminish within 2-4 weeks",
                "energy_increase": "Sustained energy throughout the day",
                "sleep_quality": "Falling asleep easily, staying asleep",
                "digestive_health": "Regular elimination, no bloating or gas",
                "emotional_balance": "Reduced anxiety, anger, or depression"
            }
        }
    
    def generate_personalized_response(self, 
                                     query: str, 
                                     user_constitution: Optional[str] = None,
                                     user_age: Optional[int] = None,
                                     current_season: str = "fall",
                                     symptoms: List[str] = None,
                                     context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate comprehensive AI response using NanoSutracore intelligence
        """
        
        # Prepare context for GPT
        system_prompt = self._build_system_prompt(user_constitution, user_age, current_season)
        user_prompt = self._build_user_prompt(query, symptoms, context)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse and structure the response
            structured_response = self._structure_response(ai_response, query, user_constitution)
            
            return structured_response
            
        except Exception as e:
            # Fallback to knowledge base response
            return self._fallback_response(query, user_constitution, current_season)
    
    def _build_system_prompt(self, constitution: str, age: int, season: str) -> str:
        """Build comprehensive system prompt with knowledge bases"""
        
        prompt = f"""You are NanoSutracore, the advanced AI reasoning system created by Dr. Helen Thomas DC, integrating her 44 years of clinical experience with traditional Ayurvedic wisdom.

KNOWLEDGE BASES INTEGRATED:
1. HEALING AIRWAVES: Dr. Helen's specialized healing methodologies and clinical protocols
2. AYURVEDA WISDOM: Traditional Ayurvedic principles from classical texts
3. CLINICAL EXPERIENCE: 44 years of practical application and patient outcomes

CORE HEALING PHILOSOPHY:
- The pulse reveals current dosha imbalances and guides treatment
- Every condition stems from dryness, heat, or stagnation
- Treatment hierarchy: remoisturize dryness, cool heat, flush stagnation
- Constitutional approach: work WITH the person's nature, not against it

CURRENT CONTEXT:
- Season: {season}
- User Constitution: {constitution if constitution else 'Unknown - recommend assessment'}
- User Age: {age if age else 'Unknown'}

RESPONSE GUIDELINES:
1. Always speak as Dr. Helen Thomas DC with authority from 44 years of experience
2. Reference specific knowledge from Healing Airwaves and Ayurveda Wisdom
3. Provide practical, actionable guidance
4. Include pulse diagnosis insights when relevant
5. Address root causes, not just symptoms
6. Incorporate seasonal and constitutional considerations
7. Include specific herbs, foods, and lifestyle recommendations
8. Always include the medical disclaimer

KNOWLEDGE BASE EXCERPTS:
{json.dumps(self.healing_airwaves_kb['core_principles'], indent=2)}

{json.dumps(self.ayurveda_wisdom_kb['tridosha_theory'], indent=2)}
"""
        return prompt
    
    def _build_user_prompt(self, query: str, symptoms: List[str], context: Dict[str, Any]) -> str:
        """Build user prompt with query and context"""
        
        prompt = f"QUERY: {query}\n\n"
        
        if symptoms:
            prompt += f"CURRENT SYMPTOMS: {', '.join(symptoms)}\n\n"
        
        if context:
            prompt += f"ADDITIONAL CONTEXT: {json.dumps(context, indent=2)}\n\n"
        
        prompt += """Please provide a comprehensive response that:
1. Addresses the specific query with clinical expertise
2. Explains the Ayurvedic perspective on the issue
3. Provides specific recommendations for diet, herbs, and lifestyle
4. Includes pulse diagnosis insights if relevant
5. Considers constitutional and seasonal factors
6. Offers practical next steps

Format your response in clear sections for easy understanding."""
        
        return prompt
    
    def _structure_response(self, ai_response: str, query: str, constitution: str) -> Dict[str, Any]:
        """Structure the AI response into organized sections"""
        
        return {
            "answer": ai_response,
            "source": "NanoSutracore AI Engine",
            "knowledge_bases": ["Healing Airwaves", "Ayurveda Wisdom", "Clinical Experience"],
            "constitution_specific": constitution is not None,
            "personalized": True,
            "clinical_authority": "Dr. Helen Thomas DC - 44 years experience",
            "timestamp": datetime.utcnow().isoformat(),
            "recommendations": self._extract_recommendations(ai_response),
            "herbs_supplements": self._extract_herbs(ai_response),
            "lifestyle_tips": self._extract_lifestyle_tips(ai_response),
            "warning": "This guidance is for educational purposes. Always consult your healthcare provider for medical advice."
        }
    
    def _extract_recommendations(self, response: str) -> List[str]:
        """Extract specific recommendations from AI response"""
        # Simple extraction - could be enhanced with NLP
        recommendations = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'try', 'consider']):
                recommendations.append(line.strip())
        return recommendations[:5]  # Limit to top 5
    
    def _extract_herbs(self, response: str) -> List[str]:
        """Extract herbs and supplements mentioned in response"""
        herbs = []
        common_herbs = [
            'ashwagandha', 'turmeric', 'ginger', 'triphala', 'brahmi', 
            'aloe vera', 'coriander', 'fennel', 'cumin', 'cardamom',
            'cinnamon', 'cloves', 'nutmeg', 'sesame oil', 'ghee'
        ]
        
        response_lower = response.lower()
        for herb in common_herbs:
            if herb in response_lower:
                herbs.append(herb.title())
        
        return list(set(herbs))  # Remove duplicates
    
    def _extract_lifestyle_tips(self, response: str) -> List[str]:
        """Extract lifestyle recommendations from response"""
        tips = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['lifestyle', 'daily', 'routine', 'practice']):
                tips.append(line.strip())
        return tips[:3]  # Limit to top 3
    
    def _fallback_response(self, query: str, constitution: str, season: str) -> Dict[str, Any]:
        """Fallback response using knowledge bases when GPT is unavailable"""
        
        # Determine query type and provide relevant knowledge base response
        query_lower = query.lower()
        
        if 'eat' in query_lower or 'food' in query_lower or 'diet' in query_lower:
            response = self._get_dietary_guidance(constitution, season)
        elif 'symptom' in query_lower or 'pain' in query_lower or 'problem' in query_lower:
            response = self._get_symptom_guidance(constitution)
        elif 'lifestyle' in query_lower or 'routine' in query_lower:
            response = self._get_lifestyle_guidance(constitution, season)
        else:
            response = self._get_general_guidance(constitution)
        
        return {
            "answer": response,
            "source": "Healing Airwaves & Ayurveda Wisdom Knowledge Bases",
            "constitution_specific": constitution is not None,
            "personalized": True,
            "clinical_authority": "Dr. Helen Thomas DC - 44 years experience",
            "recommendations": [],
            "herbs_supplements": [],
            "lifestyle_tips": [],
            "warning": "This guidance is for educational purposes. Always consult your healthcare provider for medical advice."
        }
    
    def _get_dietary_guidance(self, constitution: str, season: str) -> str:
        """Get dietary guidance from knowledge bases"""
        if not constitution:
            return "To provide personalized dietary guidance, I need to know your constitution. Please take our assessment first."
        
        const_type = constitution.split('-')[0].lower()
        if const_type in self.healing_airwaves_kb['therapeutic_approaches']:
            protocol = self.healing_airwaves_kb['therapeutic_approaches'][f'{const_type}_protocol']
            return f"For your {constitution} constitution, focus on foods that {protocol['treatment']}. Beneficial foods include: {', '.join(protocol['herbs'])}. During {season}, adjust by incorporating seasonal wisdom from my clinical experience."
        
        return "Based on my 44 years of clinical experience, dietary recommendations should be tailored to your specific constitution and current imbalances."
    
    def _get_symptom_guidance(self, constitution: str) -> str:
        """Get symptom-based guidance from knowledge bases"""
        return "From my clinical experience, symptoms are signals of dosha imbalances. The pulse diagnosis reveals whether you have dryness (Vata), heat (Pitta), or stagnation (Kapha) as the root cause. The first step is always simple: remoisturize dryness, cool heat, or flush stagnation."
    
    def _get_lifestyle_guidance(self, constitution: str, season: str) -> str:
        """Get lifestyle guidance from knowledge bases"""
        return f"Your daily routine should align with your constitution and the current {season} season. From the Healing Airwaves methodology, consistency in sleep, meals, and practices is essential for maintaining dosha balance."
    
    def _get_general_guidance(self, constitution: str) -> str:
        """Get general Ayurvedic guidance"""
        return "From my 44 years in the clinic teaching Ayurveda, I've learned that healing is remembering - Ayurveda is the Mother. Your constitution is your blueprint, and understanding it changes everything about how you approach health and healing."

# Global instance
nanosutracore = NanoSutracore()
