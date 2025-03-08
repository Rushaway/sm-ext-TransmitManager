#if defined _TransmitManager_included
  #endinput
#endif
#define _TransmitManager_included

/**
 * Adds an entity to the transmission management system.
 * Once added, the entity can be controlled via other API functions.
 *
 * @param entity        Index of the entity to manage.
 * @error               Invalid or already managed entity.
 */
native void TransmitManager_AddEntityHooks(int entity);

/**
 * Sets an ownership relationship between two entities.
 * When an entity is set as the owner of another, the visibility of the owner
 * affects that of the owned entity. If the owner is not visible to a player,
 * the owned entity will not be either.
 *
 * @param entity        Index of the entity to be owned.
 * @param target        Index of the owning entity. Use -1 to remove the relationship.
 * @return              true if the operation succeeded, false otherwise.
 * @error               Invalid or unmanaged entity by the extension.
 */
native bool TransmitManager_SetEntityOwner(int entity, int target);

/**
 * Sets whether a player can see an entity.
 * This function allows precise control over the visibility of an entity for a specific player.
 *
 * @param entity        Index of the entity.
 * @param client        Index of the player.
 * @param can           true to make the entity visible, false to hide it.
 * @return              true if the operation succeeded, false otherwise.
 * @error               Invalid entity or client, or unmanaged entity by the extension.
 */
native bool TransmitManager_SetEntityState(int entity, int client, bool can);

/**
 * Checks if a player can see an entity.
 * This function allows knowing the current visibility state of an entity for a player.
 *
 * @param entity        Index of the entity.
 * @param client        Index of the player.
 * @return              true if the player can see the entity, false otherwise.
 * @error               Invalid entity or client, or unmanaged entity by the extension.
 */
native bool TransmitManager_GetEntityState(int entity, int client);

/**
 * Checks if an entity is managed by the extension.
 * This function allows knowing if an entity has been added to the management system via
 * TransmitManager_AddEntityHooks().
 *
 * @param entity        Index of the entity to check.
 * @return              true if the entity is managed, false otherwise.
 * @error               Invalid entity.
 */
native bool TransmitManager_IsEntityHooked(int entity);

/**
 * _________________Do not edit below this line!_______________________
 */
public Extension __ext_transmit = 
{
	name = "TransmitManager",
	file = "TransmitManager.ext",
#if defined AUTOLOAD_EXTENSIONS
	autoload = 1,
#else
	autoload = 0,
#endif
#if defined REQUIRE_EXTENSIONS
	required = 1,
#else
	required = 0,
#endif
};
