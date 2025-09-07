export const mockRecipes = [
  {
    id: '1',
    title: 'Gentle Chicken and Rice Bowl',
    description: 'A soothing, easy-to-digest meal that was one of my first safe foods during recovery.',
    image: 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=600&h=400&fit=crop',
    prepTime: '15 min',
    cookTime: '25 min',
    servings: 4,
    difficulty: 'Easy',
    dietaryTags: ['gluten-free', 'dairy-free', 'low-fodmap'],
    ingredients: [
      '2 cups jasmine rice',
      '4 chicken thighs (boneless, skinless)',
      '3 cups low-sodium chicken broth',
      '2 tbsp olive oil',
      '1 tsp salt',
      '1/2 tsp turmeric',
      '2 carrots, diced small',
      'Fresh parsley for garnish'
    ],
    instructions: [
      'Rinse rice until water runs clear. Set aside.',
      'Season chicken with salt and turmeric.',
      'Heat olive oil in a large pot over medium heat.',
      'Cook chicken until golden, about 6 minutes per side. Remove and set aside.',
      'Add rice to the same pot, stir for 2 minutes.',
      'Add broth and bring to boil. Reduce heat and simmer covered for 18 minutes.',
      'Shred chicken and fold back into rice with carrots.',
      'Let rest 5 minutes, then garnish with parsley.'
    ],
    story: 'This was the first meal I could eat without discomfort after months of digestive issues. The gentle flavors and easily digestible ingredients made it a cornerstone of my healing journey.'
  },
  {
    id: '2',
    title: 'Healing Bone Broth',
    description: 'Nutrient-rich bone broth that soothes the gut and provides essential minerals.',
    image: 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&h=400&fit=crop',
    prepTime: '20 min',
    cookTime: '12 hours',
    servings: 8,
    difficulty: 'Easy',
    dietaryTags: ['gluten-free', 'dairy-free', 'paleo', 'keto'],
    ingredients: [
      '3 lbs beef or chicken bones',
      '2 tbsp apple cider vinegar',
      '1 onion, quartered',
      '2 celery stalks',
      '2 bay leaves',
      '1 tsp sea salt',
      '12 cups filtered water',
      'Fresh herbs (thyme, rosemary)'
    ],
    instructions: [
      'Place bones in slow cooker or large pot.',
      'Add vinegar and let sit for 30 minutes.',
      'Add remaining ingredients and cover with water.',
      'Cook on low for 12-24 hours (slow cooker) or simmer gently on stovetop.',
      'Strain through fine mesh strainer.',
      'Cool completely and refrigerate. Remove fat layer when cold.',
      'Reheat portions as needed. Can be frozen for up to 6 months.'
    ],
    story: 'Bone broth became my daily ritual. The collagen and minerals helped heal my gut lining, and the warm, comforting liquid was often all I could manage on difficult days.'
  },
  {
    id: '3',
    title: 'Simple Baked Sweet Potato',
    description: 'Perfectly baked sweet potato with gut-friendly toppings.',
    image: 'https://images.unsplash.com/photo-1518788335250-ee7a8b39f0cb?w=600&h=400&fit=crop',
    prepTime: '5 min',
    cookTime: '45 min',
    servings: 1,
    difficulty: 'Easy',
    dietaryTags: ['gluten-free', 'dairy-free', 'vegan', 'paleo'],
    ingredients: [
      '1 medium sweet potato',
      '1 tbsp olive oil',
      '1/4 tsp sea salt',
      '1 tbsp coconut oil',
      'Cinnamon to taste',
      'Optional: chopped chives'
    ],
    instructions: [
      'Preheat oven to 425°F (220°C).',
      'Wash and pierce sweet potato with fork.',
      'Rub with olive oil and salt.',
      'Bake for 45-60 minutes until tender.',
      'Cut open and fluff with fork.',
      'Top with coconut oil, cinnamon, and chives if using.'
    ],
    story: 'Sweet potatoes were one of the few foods that never caused me issues. They provided gentle energy and essential nutrients when my diet was very limited.'
  },
  {
    id: '4',
    title: 'Gentle Ginger Tea',
    description: 'Soothing ginger tea to calm digestive discomfort.',
    image: 'https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=600&h=400&fit=crop',
    prepTime: '5 min',
    cookTime: '10 min',
    servings: 1,
    difficulty: 'Easy',
    dietaryTags: ['gluten-free', 'dairy-free', 'vegan'],
    ingredients: [
      '1 inch fresh ginger root',
      '1 cup filtered water',
      '1 tsp raw honey (optional)',
      'Lemon slice (optional)'
    ],
    instructions: [
      'Peel and slice ginger root thinly.',
      'Bring water to boil in small saucepan.',
      'Add ginger slices and reduce heat.',
      'Simmer gently for 8-10 minutes.',
      'Strain into mug.',
      'Add honey and lemon if tolerated.'
    ],
    story: 'Ginger tea was my constant companion during flare-ups. The anti-inflammatory properties helped reduce nausea and settle my stomach naturally.'
  },
  {
    id: '5',
    title: 'Quinoa Porridge Bowl',
    description: 'Creamy, nutritious breakfast that is gentle on sensitive stomachs.',
    image: 'https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?w=600&h=400&fit=crop',
    prepTime: '5 min',
    cookTime: '20 min',
    servings: 2,
    difficulty: 'Easy',
    dietaryTags: ['gluten-free', 'dairy-free', 'vegan'],
    ingredients: [
      '1 cup quinoa, rinsed',
      '2 cups coconut milk',
      '1 cup water',
      '2 tbsp maple syrup',
      '1/2 tsp vanilla extract',
      '1/4 tsp cinnamon',
      'Pinch of salt',
      'Fresh berries for topping'
    ],
    instructions: [
      'Combine quinoa, coconut milk, and water in saucepan.',
      'Bring to boil, then reduce heat to low.',
      'Simmer covered for 15-20 minutes until creamy.',
      'Stir in maple syrup, vanilla, cinnamon, and salt.',
      'Serve warm topped with fresh berries.',
      'Can be refrigerated and reheated with extra liquid.'
    ],
    story: 'When oats were too harsh for my system, quinoa porridge became my go-to breakfast. It provided protein and sustained energy without digestive distress.'
  }
];

export const dietaryFilters = [
  { id: 'gluten-free', label: 'Gluten-Free', count: 5 },
  { id: 'dairy-free', label: 'Dairy-Free', count: 5 },
  { id: 'low-fodmap', label: 'Low-FODMAP', count: 1 },
  { id: 'vegan', label: 'Vegan', count: 3 },
  { id: 'paleo', label: 'Paleo', count: 2 },
  { id: 'keto', label: 'Keto', count: 1 }
];

export const personalStory = {
  title: "My Healing Journey",
  subtitle: "From digestive distress to gut-friendly nourishment",
  content: [
    "Three years ago, I found myself in a place many of you might recognize - struggling with severe digestive issues that left me afraid to eat. What started as occasional discomfort had evolved into daily pain, bloating, and a growing list of foods that seemed to trigger symptoms.",
    "After months of elimination diets, medical consultations, and countless nights researching gut health, I realized that healing would require more than just removing problematic foods. I needed to rebuild my relationship with nourishment entirely.",
    "The recipes you'll find here aren't just meals - they're stepping stones on a healing journey. Each dish was carefully crafted during my recovery, tested not just for taste, but for how gentle they were on my sensitive system. Some became daily staples, others were comfort foods for difficult days.",
    "I'm sharing these recipes because I know how isolating digestive issues can feel, and how overwhelming it can be to figure out what's safe to eat. My hope is that these simple, nourishing meals can provide you with both physical comfort and the reassurance that healing is possible."
  ],
  image: "https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=600&h=400&fit=crop"
};