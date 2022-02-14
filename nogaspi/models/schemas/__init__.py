from .register import LoginInputSchema, LogoutInputSchema, CheckTokenValidityInputSchema
from .food import (
    GetProductInputSchema,
    PostDonationFromScanInputSchema,
    PostDonationFromFridgeInputSchema,
    DeleteMyDonationsInputSchema,
    GetDonationsInputSchema,
    GetDonationByIdInputSchema,
    GetDonationsByRegularPathInputSchema,
    GetAllergensInputSchema,
    PostArticlesInFridgeInputSchema,
    DeleteArticlesInFridgeInputSchema,
    GetArticlesInFridgeInputSchema,
    TakeDonationsInputSchema,
    GenerateDonationsCodeInputSchema,
    GetFavoriteDonationsInputSchema,
    ToggleDonationInMyFavoriteInputSchema,
    GetMyDonationsInputSchema,
)
from .user import (
    PostRegularPathInputSchema,
    GetRegularPathInputSchema,
    PostFireBaseTokenInputSchema
)

from .tools import GetProfilePictureInputSchema

from .messaging import (
    InitiateConversationInputSchema,
    PostMessageInputSchema,
    AcknowledgeMessagesOnConversationInputSchema,
    GetMyConversationsInputSchema,
    GetConversationInputSchema,
    GetConversationsByDonationInputSchema
)