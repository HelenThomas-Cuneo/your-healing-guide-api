"""
Enhanced AI Query Processor for Ayurvedic and Vedic Astrology Guidance
Integrating NanoSutracore with comprehensive knowledge bases
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from .ayurveda_astrology_kb import ayurveda_astrology_kb

class EnhancedQueryProcessor:
    """Advanced query processor for Ayurvedic and astrological guidance"""
    
    def __init__(self):
        self.kb = ayurveda_astrology_kb
        self.query_patterns = self._load_query_patterns()
        self.clinical_wisdom = self._load_clinical_wisdom()
    
    def _load_query_patterns(self) -> Dict:
        """Load query pattern recognition for different types of questions"""
        return {
            "constitutional": [
                r"what.*constitution.*am.*i",
                r"my.*body.*type",
                r"dosha.*analysis",
                r"vata.*pitta.*kapha",
                r"ayurvedic.*type"
            ],
            "symptoms": [
                r"i.*have.*symptoms?",
                r"experiencing.*problems?",
                r"feeling.*unwell",
                r"health.*issues?",
                r"pain.*in.*"
            ],
            "dietary": [
                r"what.*should.*i.*eat",
                r"food.*recommendations?",
                r"diet.*for.*",
                r"nutrition.*advice",
                r"avoid.*eating"
            ],
            "lifestyle": [
                r"lifestyle.*changes?",
                r"daily.*routine",
                r"exercise.*recommendations?",
                r"sleep.*advice",
                r"stress.*management"
            ],
            "seasonal": [
                r"current.*season",
                r"winter.*summer.*spring.*fall",
                r"seasonal.*advice",
                r"weather.*affecting",
                r"time.*of.*year"
            ],
            "astrological": [
                r"planetary.*influence",
                r"vedic.*astrology",
                r"birth.*chart",
                r"planets?.*affecting",
                r"astrological.*remedy"
            ],
            "herbs": [
                r"herbs?.*for.*",
                r"supplements?.*recommendations?",
                r"natural.*remedies?",
                r"ayurvedic.*medicine",
                r"herbal.*treatment"
            ],
            "age_related": [
                r"my.*age.*is",
                r"i.*am.*years.*old",
                r"life.*stage",
                r"aging.*concerns?",
                r"elderly.*care"
            ]
        }
    
    def _load_clinical_wisdom(self) -> Dict:
        """Dr. Helen's clinical wisdom and treatment approaches"""
        return {
            "diagnostic_approach": {
                "pulse_reading": "First, I assess the pulse quality - is it moving like a snake (vata), frog (pitta), or swan (kapha)?",
                "tongue_examination": "The tongue reveals much about digestion and dosha balance",
                "constitutional_assessment": "Understanding your prakruti (birth constitution) vs vikruti (current imbalance)",
                "lifestyle_analysis": "How your daily routine affects your doshic balance"
            },
            
            "treatment_philosophy": {
                "root_cause": "We treat the root cause, not just symptoms",
                "individual_approach": "Each person is unique - no one-size-fits-all solutions",
                "gradual_healing": "Healing happens in layers, be patient with the process",
                "prevention": "Prevention is always better than cure"
            },
            
            "common_patterns": {
                "modern_lifestyle": "Most people today have vata imbalances from stress and irregular routines",
                "digestive_fire": "Weak agni (digestive fire) is at the root of most diseases",
                "seasonal_awareness": "Many health issues can be prevented by living in harmony with seasons",
                "mind_body_connection": "Mental and emotional states directly affect physical health"
            }
        }
    
    def process_query(self, query: str, user_data: Dict = None) -> Dict:
        """Process user query and provide comprehensive guidance"""
        
        # Extract query type and key information
        query_analysis = self._analyze_query(query)
        
        # Get user context
        user_context = self._extract_user_context(user_data or {})
        
        # Generate response based on query type
        response = self._generate_comprehensive_response(query, query_analysis, user_context)
        
        return response
    
    def _analyze_query(self, query: str) -> Dict:
        """Analyze query to determine type and extract key information"""
        query_lower = query.lower()
        
        analysis = {
            "query_types": [],
            "keywords": [],
            "symptoms": [],
            "body_parts": [],
            "emotions": [],
            "time_references": [],
            "constitution_mentions": []
        }
        
        # Identify query types
        for query_type, patterns in self.query_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    analysis["query_types"].append(query_type)
                    break
        
        # Extract specific keywords
        analysis["keywords"] = self._extract_keywords(query_lower)
        analysis["symptoms"] = self._extract_symptoms(query_lower)
        analysis["body_parts"] = self._extract_body_parts(query_lower)
        analysis["emotions"] = self._extract_emotions(query_lower)
        analysis["constitution_mentions"] = self._extract_constitution_mentions(query_lower)
        
        return analysis
    
    def _extract_user_context(self, user_data: Dict) -> Dict:
        """Extract relevant user context for personalized guidance"""
        context = {
            "constitution": user_data.get("constitution"),
            "age": user_data.get("age"),
            "current_season": self._get_current_season(),
            "life_stage": self._determine_life_stage(user_data.get("age")),
            "previous_assessments": user_data.get("assessments", []),
            "health_goals": user_data.get("health_goals", [])
        }
        
        return context
    
    def _generate_comprehensive_response(self, query: str, analysis: Dict, context: Dict) -> Dict:
        """Generate comprehensive response using all available knowledge"""
        
        response = {
            "answer": "",
            "constitutional_guidance": {},
            "astrological_insights": {},
            "seasonal_recommendations": {},
            "clinical_wisdom": "",
            "herbs_and_supplements": [],
            "lifestyle_modifications": [],
            "dietary_guidance": [],
            "follow_up_questions": [],
            "confidence_level": "high",
            "source": "Dr. Helen Thomas DC - 44 years clinical experience + NanoSutracore AI"
        }
        
        # Generate main answer based on query types
        if "constitutional" in analysis["query_types"]:
            response.update(self._handle_constitutional_query(query, analysis, context))
        
        if "symptoms" in analysis["query_types"]:
            response.update(self._handle_symptoms_query(query, analysis, context))
        
        if "dietary" in analysis["query_types"]:
            response.update(self._handle_dietary_query(query, analysis, context))
        
        if "astrological" in analysis["query_types"]:
            response.update(self._handle_astrological_query(query, analysis, context))
        
        if "seasonal" in analysis["query_types"]:
            response.update(self._handle_seasonal_query(query, analysis, context))
        
        if "herbs" in analysis["query_types"]:
            response.update(self._handle_herbs_query(query, analysis, context))
        
        # Add clinical wisdom and personalization
        response["clinical_wisdom"] = self._add_clinical_wisdom(analysis, context)
        response["follow_up_questions"] = self._generate_follow_up_questions(analysis, context)
        
        # Ensure main answer is comprehensive
        if not response["answer"]:
            response["answer"] = self._generate_general_guidance(query, analysis, context)
        
        return response
    
    def _handle_constitutional_query(self, query: str, analysis: Dict, context: Dict) -> Dict:
        """Handle constitution-related queries"""
        constitution = context.get("constitution")
        
        if constitution:
            const_analysis = self.kb.get_constitutional_analysis(constitution, analysis.get("symptoms", []))
            
            return {
                "answer": f"Based on your {constitution} constitution, here's what I observe from my 44 years of clinical experience...",
                "constitutional_guidance": const_analysis,
                "personalized": True
            }
        else:
            return {
                "answer": "To provide accurate constitutional guidance, I recommend taking our comprehensive 13-constitution assessment first. This will help me give you personalized recommendations based on your unique body type.",
                "constitutional_guidance": {"recommendation": "Take constitutional assessment"},
                "personalized": False
            }
    
    def _handle_symptoms_query(self, query: str, analysis: Dict, context: Dict) -> Dict:
        """Handle symptom-related queries"""
        symptoms = analysis.get("symptoms", [])
        constitution = context.get("constitution")
        
        response_data = {
            "answer": "Let me analyze your symptoms from an Ayurvedic perspective...",
            "symptom_analysis": {},
            "recommendations": []
        }
        
        if constitution and symptoms:
            # Analyze symptoms in constitutional context
            symptom_analysis = self._analyze_symptoms_by_constitution(symptoms, constitution)
            response_data["symptom_analysis"] = symptom_analysis
            response_data["answer"] = f"For your {constitution} constitution, these symptoms suggest..."
        
        return response_data
    
    def _handle_dietary_query(self, query: str, analysis: Dict, context: Dict) -> Dict:
        """Handle dietary and nutrition queries"""
        constitution = context.get("constitution")
        season = context.get("current_season")
        
        dietary_guidance = []
        
        if constitution:
            const_data = self.kb.get_constitutional_analysis(constitution)
            dietary_guidance.extend(const_data.get("balancing_foods", []))
        
        if season:
            seasonal_data = self.kb.get_seasonal_recommendations(season, constitution or "general")
            dietary_guidance.extend(seasonal_data.get("foods_to_favor", []))
        
        return {
            "answer": f"Based on your constitution and the current season, here are my dietary recommendations...",
            "dietary_guidance": dietary_guidance,
            "foods_to_avoid": seasonal_data.get("foods_to_avoid", []) if season else [],
            "meal_timing": self._get_meal_timing_advice(constitution)
        }
    
    def _handle_astrological_query(self, query: str, analysis: Dict, context: Dict) -> Dict:
        """Handle Vedic astrology queries"""
        # Extract planetary references from query
        planets = self._extract_planetary_references(query)
        constitution = context.get("constitution")
        
        astrological_insights = {}
        
        for planet in planets:
            planet_guidance = self.kb.get_planetary_guidance(planet, constitution)
            astrological_insights[planet] = planet_guidance
        
        return {
            "answer": "From a Vedic astrology perspective, here's how planetary influences may be affecting your health...",
            "astrological_insights": astrological_insights,
            "remedial_measures": self._compile_remedial_measures(planets)
        }
    
    def _handle_seasonal_query(self, query: str, analysis: Dict, context: Dict) -> Dict:
        """Handle seasonal health queries"""
        season = context.get("current_season")
        constitution = context.get("constitution")
        
        if season and constitution:
            seasonal_recs = self.kb.get_seasonal_recommendations(season, constitution)
            
            return {
                "answer": f"For the {season} season and your {constitution} constitution, here's my guidance...",
                "seasonal_recommendations": seasonal_recs,
                "seasonal_herbs": seasonal_recs.get("seasonal_herbs", [])
            }
        
        return {
            "answer": "Seasonal health depends on your constitution. Let me provide general seasonal guidance...",
            "seasonal_recommendations": self.kb.get_seasonal_recommendations(season or "current", "general")
        }
    
    def _handle_herbs_query(self, query: str, analysis: Dict, context: Dict) -> Dict:
        """Handle herbal medicine queries"""
        constitution = context.get("constitution")
        symptoms = analysis.get("symptoms", [])
        
        herb_recommendations = []
        
        if constitution:
            const_data = self.kb.get_constitutional_analysis(constitution)
            herb_recommendations.extend(const_data.get("recommended_herbs", []))
        
        # Add symptom-specific herbs
        symptom_herbs = self._get_herbs_for_symptoms(symptoms, constitution)
        herb_recommendations.extend(symptom_herbs)
        
        return {
            "answer": "Based on your constitution and symptoms, here are my herbal recommendations...",
            "herbs_and_supplements": list(set(herb_recommendations)),  # Remove duplicates
            "preparation_methods": self._get_herb_preparation_methods(herb_recommendations),
            "precautions": "Always consult with a qualified practitioner before starting herbal treatments."
        }
    
    def _add_clinical_wisdom(self, analysis: Dict, context: Dict) -> str:
        """Add Dr. Helen's clinical wisdom to the response"""
        wisdom_points = []
        
        # Add relevant clinical observations
        if "symptoms" in analysis["query_types"]:
            wisdom_points.append("In my 44 years of practice, I've found that symptoms are the body's way of communicating imbalance.")
        
        if context.get("constitution"):
            wisdom_points.append(f"Your {context['constitution']} constitution gives us important clues about your healing path.")
        
        wisdom_points.append("Remember, Ayurveda teaches us that healing happens in layers - be patient with the process.")
        
        return " ".join(wisdom_points)
    
    def _generate_follow_up_questions(self, analysis: Dict, context: Dict) -> List[str]:
        """Generate relevant follow-up questions"""
        questions = []
        
        if not context.get("constitution"):
            questions.append("Would you like to take our 13-constitution assessment for personalized guidance?")
        
        if "symptoms" in analysis["query_types"]:
            questions.append("How long have you been experiencing these symptoms?")
            questions.append("Have you noticed any patterns with your symptoms?")
        
        if "dietary" in analysis["query_types"]:
            questions.append("What does your typical daily meal schedule look like?")
        
        questions.append("Are there any specific health goals you're working toward?")
        
        return questions[:3]  # Limit to 3 questions
    
    def _generate_general_guidance(self, query: str, analysis: Dict, context: Dict) -> str:
        """Generate general guidance when specific handlers don't apply"""
        return f"Thank you for your question about {query}. From my 44 years of clinical experience with Ayurveda, I can share that every health concern has roots in constitutional imbalance. Let me provide some guidance based on traditional Ayurvedic principles..."
    
    # Helper methods
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from query"""
        # Implementation for keyword extraction
        return []
    
    def _extract_symptoms(self, query: str) -> List[str]:
        """Extract symptoms mentioned in query"""
        symptom_keywords = ["pain", "ache", "tired", "fatigue", "insomnia", "anxiety", "depression", "headache", "nausea", "bloating", "constipation", "diarrhea"]
        found_symptoms = []
        for symptom in symptom_keywords:
            if symptom in query:
                found_symptoms.append(symptom)
        return found_symptoms
    
    def _extract_body_parts(self, query: str) -> List[str]:
        """Extract body parts mentioned in query"""
        body_parts = ["head", "heart", "stomach", "back", "joints", "skin", "eyes", "throat", "chest", "abdomen"]
        found_parts = []
        for part in body_parts:
            if part in query:
                found_parts.append(part)
        return found_parts
    
    def _extract_emotions(self, query: str) -> List[str]:
        """Extract emotional states mentioned in query"""
        emotions = ["anxious", "stressed", "angry", "sad", "depressed", "worried", "fearful", "irritated"]
        found_emotions = []
        for emotion in emotions:
            if emotion in query:
                found_emotions.append(emotion)
        return found_emotions
    
    def _extract_constitution_mentions(self, query: str) -> List[str]:
        """Extract constitution types mentioned in query"""
        constitutions = ["vata", "pitta", "kapha"]
        found_constitutions = []
        for const in constitutions:
            if const in query:
                found_constitutions.append(const)
        return found_constitutions
    
    def _extract_planetary_references(self, query: str) -> List[str]:
        """Extract planetary references from query"""
        planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
        found_planets = []
        for planet in planets:
            if planet in query.lower():
                found_planets.append(planet)
        return found_planets
    
    def _get_current_season(self) -> str:
        """Determine current season"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "fall"
        else:
            return "winter"
    
    def _determine_life_stage(self, age: Optional[int]) -> str:
        """Determine life stage based on age"""
        if not age:
            return "unknown"
        elif age < 16:
            return "childhood"
        elif age < 50:
            return "youth"
        else:
            return "maturity"
    
    def _analyze_symptoms_by_constitution(self, symptoms: List[str], constitution: str) -> Dict:
        """Analyze symptoms in context of constitution"""
        return {
            "constitutional_correlation": f"Symptoms analyzed for {constitution} constitution",
            "likely_imbalances": ["Analysis based on clinical experience"],
            "treatment_approach": "Constitutional balancing recommended"
        }
    
    def _get_meal_timing_advice(self, constitution: str) -> Dict:
        """Get meal timing advice for constitution"""
        if constitution and "vata" in constitution.lower():
            return {"advice": "Regular meal times are crucial for vata constitution"}
        elif constitution and "pitta" in constitution.lower():
            return {"advice": "Don't skip meals, especially lunch - your digestive fire is strongest then"}
        elif constitution and "kapha" in constitution.lower():
            return {"advice": "Light breakfast, substantial lunch, light dinner works best"}
        return {"advice": "Regular meal timing supports all constitutions"}
    
    def _get_herbs_for_symptoms(self, symptoms: List[str], constitution: str) -> List[str]:
        """Get herbs specific to symptoms and constitution"""
        herbs = []
        if "anxiety" in symptoms:
            herbs.extend(["Brahmi", "Jatamansi", "Ashwagandha"])
        if "digestive" in symptoms or "bloating" in symptoms:
            herbs.extend(["Triphala", "Ginger", "Fennel"])
        return herbs
    
    def _get_herb_preparation_methods(self, herbs: List[str]) -> Dict:
        """Get preparation methods for herbs"""
        return {
            "general": "Most herbs can be taken as tea, powder, or capsules",
            "specific": "Consult with practitioner for specific preparations"
        }
    
    def _compile_remedial_measures(self, planets: List[str]) -> List[str]:
        """Compile remedial measures for planets"""
        measures = []
        for planet in planets:
            planet_data = self.kb.get_planetary_guidance(planet)
            measures.extend(planet_data.get("remedial_measures", []))
        return list(set(measures))  # Remove duplicates

# Initialize the enhanced query processor
enhanced_query_processor = EnhancedQueryProcessor()
